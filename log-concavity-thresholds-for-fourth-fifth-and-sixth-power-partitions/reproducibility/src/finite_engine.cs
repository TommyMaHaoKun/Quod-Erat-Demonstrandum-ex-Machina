// Exact power-partition coefficient and determinant engine, C# 5 / .NET 4+.
// No floating arithmetic enters a coefficient or determinant sign.
using System;
using System.IO;
using System.Numerics;
using System.Security.Cryptography;
using System.Diagnostics;

public static class FiniteEngine {
    const int ChunkBytes = 4 * 1024 * 1024;
    static int Pow(int a, int k) { long v=1; for(int i=0;i<k;i++) v*=a; return v>int.MaxValue?int.MaxValue:(int)v; }
    static string Hash(string path) { using(var f=File.OpenRead(path)) using(var h=SHA256.Create()) return BitConverter.ToString(h.ComputeHash(f)).Replace("-", "").ToLowerInvariant(); }
    static void Save(ulong[] a,string path) {
        byte[] b=new byte[ChunkBytes];
        using(var f=new FileStream(path,FileMode.Create,FileAccess.Write,FileShare.None,ChunkBytes)) {
            long size=8L*a.Length;
            for(long p=0;p<size;p+=b.Length) {int len=(int)Math.Min(b.Length,size-p); Buffer.BlockCopy(a,(int)p,b,0,len); f.Write(b,0,len);}
            f.Flush(true);
        }
    }
    static void Load(ulong[] a,string path) {
        byte[] b=new byte[ChunkBytes]; long size=8L*a.Length;
        using(var f=File.OpenRead(path)) {
            if(f.Length!=size) throw new Exception("Checkpoint size mismatch");
            for(long p=0;p<size;p+=b.Length) {int len=(int)Math.Min(b.Length,size-p),got=0; while(got<len) {int r=f.Read(b,got,len-got); if(r==0)throw new Exception("Truncated checkpoint");got+=r;} Buffer.BlockCopy(b,0,a,(int)p,len);}
        }
    }
    // Exact unsigned 64x64 -> 128 multiplication, four 32-bit partial products.
    static void Mul64(ulong a,ulong b,out ulong lo,out ulong hi) {
        ulong a0=(uint)a,a1=a>>32,b0=(uint)b,b1=b>>32;
        ulong w0=a0*b0,t=a1*b0+(w0>>32),w1=(uint)t,w2=t>>32;
        w1+=a0*b1; hi=a1*b1+w2+(w1>>32);lo=(w1<<32)+(uint)w0;
    }
    static ulong Add(ref ulong x,ulong y) {ulong z=x+y;ulong c=z<x?1UL:0UL;x=z;return c;}
    static void Mul128(ulong a0,ulong a1,ulong b0,ulong b1,ulong[] r) {
        ulong l00,h00,l01,h01,l10,h10,l11,h11;
        Mul64(a0,b0,out l00,out h00);Mul64(a0,b1,out l01,out h01);Mul64(a1,b0,out l10,out h10);Mul64(a1,b1,out l11,out h11);
        r[0]=l00;r[1]=h00;ulong c1=Add(ref r[1],l01)+Add(ref r[1],l10);
        r[2]=h01;ulong c2=Add(ref r[2],h10)+Add(ref r[2],l11)+Add(ref r[2],c1);
        r[3]=h11+c2;if(r[3]<h11)throw new Exception("Impossible 256-bit overflow");
    }
    static BigInteger B(ulong lo,ulong hi) {return new BigInteger(lo)+(new BigInteger(hi)<<64);}
    static BigInteger ProductValue(ulong[] r) {BigInteger x=0;for(int i=3;i>=0;i--)x=(x<<64)+r[i];return x;}
    static void SelfTest() {
        var rand=new Random(142857);byte[] buf=new byte[32];ulong[] r=new ulong[4];
        for(int i=0;i<20000;i++) {
            rand.NextBytes(buf);ulong a=BitConverter.ToUInt64(buf,0),b=BitConverter.ToUInt64(buf,8),c=BitConverter.ToUInt64(buf,16),d=BitConverter.ToUInt64(buf,24);
            if(i==0)a=b=c=d=ulong.MaxValue;
            Mul128(a,b,c,d,r);if(ProductValue(r)!=B(a,b)*B(c,d))throw new Exception("Multiplication selftest failed");
        }
    }
    public static int Main(string[] args) {
      try {
        if(args.Length!=3)throw new Exception("Usage: finite_engine.exe K MAX_DETERMINANT OUTDIR");
        if(!BitConverter.IsLittleEndian)throw new Exception("This binary format requires little-endian host");
        int k=int.Parse(args[0]),bound=int.Parse(args[1]),limit=checked(bound+1);string dir=Path.GetFullPath(args[2]);Directory.CreateDirectory(dir);
        SelfTest(); var timer=Stopwatch.StartNew();
        // Two 64-bit limbs, least significant first. Overflow is explicitly checked.
        ulong[] a=new ulong[checked(2*(limit+1))];int completed=0;string state=Path.Combine(dir,"checkpoint.txt"),old=null;
        if(File.Exists(state)) {
            string[] s=File.ReadAllLines(state);if(int.Parse(s[0])!=k||int.Parse(s[1])!=bound)throw new Exception("Checkpoint parameters differ");completed=int.Parse(s[2]);old=Path.Combine(dir,s[3]);
            if(Hash(old)!=s[4])throw new Exception("Checkpoint digest mismatch");Load(a,old);Console.WriteLine("RESUME coin="+completed);
        } else a[0]=1;
        int last=0;while(Pow(last+1,k)<=limit)last++;
        for(int j=completed+1;j<=last;j++) {
            int coin=Pow(j,k);
            for(int n=coin;n<=limit;n++) {
                int p=2*n,q=2*(n-coin);ulong lo=a[p]+a[q],carry=lo<a[p]?1UL:0UL,hi=a[p+1]+a[q+1];
                if(hi<a[p+1])throw new Exception("128-bit coefficient overflow at "+n);ulong h2=hi+carry;if(h2<hi)throw new Exception("128-bit carry overflow at "+n);
                a[p]=lo;a[p+1]=h2;
            }
            string file=Path.Combine(dir,"checkpoint_coin_"+j+".bin");Save(a,file);string sha=Hash(file);
            File.WriteAllLines(state+".tmp",new string[]{k.ToString(),bound.ToString(),j.ToString(),Path.GetFileName(file),sha});
            if(File.Exists(state))File.Delete(state);File.Move(state+".tmp",state);
            if(old!=null&&old!=file)File.Delete(old);old=file;
            Console.WriteLine("COIN "+j+"/"+last+" power="+coin+" elapsed="+timer.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();
        }
        string coefficients=Path.Combine(dir,"coefficients_u128le.bin");
        if(old!=coefficients) {if(File.Exists(coefficients))File.Delete(coefficients);File.Move(old,coefficients);File.WriteAllLines(state,new string[]{k.ToString(),bound.ToString(),last.ToString(),Path.GetFileName(coefficients),Hash(coefficients)});}
        long negatives=0,zeros=0;int lastNeg=0,lastZero=0;ulong[] left=new ulong[4],right=new ulong[4];
        using(var signs=new FileStream(Path.Combine(dir,"signs_i8.bin"),FileMode.Create,FileAccess.Write,FileShare.None,ChunkBytes)) {
            byte[] block=new byte[1000000];int used=0;
            for(int n=1;n<=bound;n++) {
                int p=2*n;Mul128(a[p],a[p+1],a[p],a[p+1],left);Mul128(a[p-2],a[p-1],a[p+2],a[p+3],right);
                int sign=0;for(int m=3;m>=0;m--)if(left[m]!=right[m]) {sign=left[m]<right[m]?-1:1;break;}
                if(sign<0){negatives++;lastNeg=n;}else if(sign==0){zeros++;lastZero=n;}
                block[used++]=unchecked((byte)(sbyte)sign);if(used==block.Length){signs.Write(block,0,used);used=0;Console.WriteLine("SCAN "+n+" elapsed="+timer.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();}
            }
            if(used>0)signs.Write(block,0,used);
        }
        using(var f=new StreamWriter(Path.Combine(dir,"summary.tsv"))) {
            f.WriteLine("k\t"+k);f.WriteLine("max_determinant_index\t"+bound);f.WriteLine("max_coefficient_index\t"+limit);f.WriteLine("negative_count\t"+negatives);f.WriteLine("equality_count\t"+zeros);f.WriteLine("largest_negative_index\t"+lastNeg);f.WriteLine("largest_equality_index\t"+lastZero);f.WriteLine("coefficients_sha256\t"+Hash(coefficients));f.WriteLine("signs_sha256\t"+Hash(Path.Combine(dir,"signs_i8.bin")));f.WriteLine("elapsed_seconds\t"+timer.Elapsed.TotalSeconds.ToString("F3"));
            int candidate=k==4?637855:k==5?2507861:35577569;
            for(int n=candidate-2;n<=candidate+1&&n<=limit;n++)if(n>=0)f.WriteLine("coefficient_"+n+"\t"+B(a[2*n],a[2*n+1]));
            for(int n=candidate-1;n<=candidate&&n<=bound;n++)if(n>0)f.WriteLine("determinant_"+n+"\t"+(B(a[2*n],a[2*n+1])*B(a[2*n],a[2*n+1])-B(a[2*n-2],a[2*n-1])*B(a[2*n+2],a[2*n+3])));
        }
        Console.WriteLine("DONE negative="+negatives+" equality="+zeros+" last_negative="+lastNeg+" last_equality="+lastZero);return 0;
      } catch(Exception e) {Console.Error.WriteLine(e);return 1;}
    }
}
