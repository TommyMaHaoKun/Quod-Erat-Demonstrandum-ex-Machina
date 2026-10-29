// Independently written finite checker. Reverse coin order, 32-bit coefficient
// limbs, and System.Numerics.BigInteger for EVERY determinant comparison.
using System;
using System.IO;
using System.IO.Compression;
using System.Numerics;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.Diagnostics;

public static class FiniteChecker {
    static BigInteger Number(uint[] p,int n) {int i=4*n;ulong low=p[i]+((ulong)p[i+1]<<32),high=p[i+2]+((ulong)p[i+3]<<32);return new BigInteger(low)+(new BigInteger(high)<<64);}
    static string Hex(byte[] a) {return BitConverter.ToString(a).Replace("-", "").ToLowerInvariant();}
    static string CoefficientHash(uint[] p) {
        byte[] buffer=new byte[4*1024*1024];long bytes=4L*p.Length;
        using(var hash=SHA256.Create()) {
            for(long offset=0;offset<bytes;offset+=buffer.Length) {int count=(int)Math.Min(buffer.Length,bytes-offset);Buffer.BlockCopy(p,(int)offset,buffer,0,count);hash.TransformBlock(buffer,0,count,null,0);}
            hash.TransformFinalBlock(new byte[0],0,0);return Hex(hash.Hash);
        }
    }
    public static int Main(string[] args) {
      try {
        if(args.Length!=1)throw new Exception("Usage: finite_checker.exe CERTIFICATE_DIRECTORY");
        if(!BitConverter.IsLittleEndian)throw new Exception("Expected little-endian host");
        string dir=Path.GetFullPath(args[0]);var expected=new Dictionary<string,string>();
        foreach(string line in File.ReadAllLines(Path.Combine(dir,"summary.tsv"))) {string[] item=line.Split('\t');expected.Add(item[0],item[1]);}
        int k=int.Parse(expected["k"]),end=int.Parse(expected["max_coefficient_index"]),bound=int.Parse(expected["max_determinant_index"]);
        if(end!=bound+1)throw new Exception("Coverage mismatch");
        var clock=Stopwatch.StartNew();var coins=new List<int>();
        for(int j=1;;j++) {long power=1;for(int h=0;h<k;h++)power*=j;if(power>end)break;coins.Add((int)power);}
        uint[] counts=new uint[checked(4*(end+1))];counts[0]=1;
        for(int c=coins.Count-1;c>=0;c--) {
            int coin=coins[c];
            for(int n=coin;n<=end;n++) {
                int a=4*n,b=4*(n-coin);ulong carry=0;
                for(int h=0;h<4;h++) {ulong sum=(ulong)counts[a+h]+counts[b+h]+carry;counts[a+h]=(uint)sum;carry=sum>>32;}
                if(carry!=0)throw new Exception("Coefficient overflow at "+n);
            }
            Console.WriteLine("CHECK COIN "+coin+" remaining="+c+" seconds="+clock.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();
        }
        string coefficientHash=CoefficientHash(counts);if(coefficientHash!=expected["coefficients_sha256"])throw new Exception("Independent full coefficient digest mismatch");
        Console.WriteLine("FULL COEFFICIENT DIGEST PASS");Console.Out.Flush();
        long negatives=0,zeros=0;int lastNegative=0,lastZero=0;string signsHash;
        BigInteger before=Number(counts,0),current=Number(counts,1);
        string compressed=Path.Combine(Directory.GetParent(dir).FullName,"finite_k"+k+"_"+bound+"_signs_i8.bin.gz");
        Stream reference=File.Exists(compressed)?(Stream)new GZipStream(File.OpenRead(compressed),CompressionMode.Decompress):File.OpenRead(Path.Combine(dir,"signs_i8.bin"));
        using(var signReference=new BufferedStream(reference,4*1024*1024))
        using(var hash=SHA256.Create()) {
            byte[] block=new byte[1000000];int used=0;
            for(int n=1;n<=bound;n++) {
                BigInteger after=Number(counts,n+1);int sign=(current*current-before*after).Sign;
                if(signReference.ReadByte()!=unchecked((byte)(sbyte)sign))throw new Exception("Exact sign-stream comparison failed at "+n);
                block[used++]=unchecked((byte)(sbyte)sign);if(sign<0){negatives++;lastNegative=n;}else if(sign==0){zeros++;lastZero=n;}
                before=current;current=after;
                if(used==block.Length) {hash.TransformBlock(block,0,used,null,0);used=0;Console.WriteLine("CHECK SIGN "+n+" seconds="+clock.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();}
            }
            if(signReference.ReadByte()!=-1)throw new Exception("Extra sign-stream bytes");
            hash.TransformFinalBlock(block,0,used);signsHash=Hex(hash.Hash);
        }
        if(signsHash!=expected["signs_sha256"])throw new Exception("Independent arbitrary-precision determinant digest mismatch");
        if(negatives!=long.Parse(expected["negative_count"])||zeros!=long.Parse(expected["equality_count"])||lastNegative!=int.Parse(expected["largest_negative_index"])||lastZero!=int.Parse(expected["largest_equality_index"]))throw new Exception("Sign count mismatch");
        foreach(var item in expected) {
            if(item.Key.StartsWith("coefficient_")) {int n=int.Parse(item.Key.Substring(12));if(Number(counts,n)!=BigInteger.Parse(item.Value))throw new Exception("Witness coefficient mismatch");}
            if(item.Key.StartsWith("determinant_")) {int n=int.Parse(item.Key.Substring(12));if(Number(counts,n)*Number(counts,n)-Number(counts,n-1)*Number(counts,n+1)!=BigInteger.Parse(item.Value))throw new Exception("Witness determinant mismatch");}
        }
        // Independent logarithmic-derivative identity on a prefix, using
        // arbitrary-precision integers; identifies p_k(n) inductively.
        int prefix=Math.Min(end,8192);long[] divisor=new long[prefix+1];
        foreach(int coin in coins)for(int n=coin;n<=prefix;n+=coin)divisor[n]+=coin;
        BigInteger[] exact=new BigInteger[prefix+1];exact[0]=BigInteger.One;
        for(int n=1;n<=prefix;n++) {
            BigInteger numerator=0;for(int m=1;m<=n;m++)numerator+=divisor[m]*exact[n-m];
            BigInteger remainder;exact[n]=BigInteger.DivRem(numerator,new BigInteger(n),out remainder);
            if(remainder!=0||exact[n]!=Number(counts,n))throw new Exception("Divisor recurrence mismatch "+n);
        }
        File.WriteAllLines(Path.Combine(dir,"independent_check.tsv"),new string[]{"result\tPASS","coefficient_range\t0.."+end,"determinant_range\t1.."+bound,"divisor_recurrence_range\t0.."+prefix,"coefficients_sha256\t"+coefficientHash,"signs_sha256\t"+signsHash,"seconds\t"+clock.Elapsed.TotalSeconds.ToString("F3"),"runtime\t"+Environment.Version});
        Console.WriteLine("PASS full reverse-order 32-bit-limb recurrence, every BigInteger determinant, independent divisor prefix="+prefix+" seconds="+clock.Elapsed.TotalSeconds.ToString("F3"));return 0;
      } catch(Exception e) {Console.Error.WriteLine(e);return 1;}
    }
}
