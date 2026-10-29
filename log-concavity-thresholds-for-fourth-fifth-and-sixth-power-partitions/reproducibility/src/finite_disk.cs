// Bounded-memory exact finite computation; C# 5 / .NET Framework 4+.
// generate: ascending parts, two 64-bit limbs; verify: descending parts,
// four 32-bit limbs. Every determinant uses arbitrary-precision BigInteger.
// Each coin is an append-only output file. Committed blocks have SHA-256
// checksums. Resume truncates any uncommitted suffix, so no update is repeated.
using System;
using System.IO;
using System.IO.Compression;
using System.Numerics;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.Diagnostics;

public static class FiniteDisk {
    static string Hex(byte[] b) {return BitConverter.ToString(b).Replace("-", "").ToLowerInvariant();}
    static string Hash(string p) {using(var f=File.OpenRead(p))using(var h=SHA256.Create())return Hex(h.ComputeHash(f));}
    static string BlockHash(byte[] b,int count) {using(var h=SHA256.Create())return Hex(h.ComputeHash(b,0,count));}
    static void ReadExact(Stream f,byte[] b,int count) {int got=0;while(got<count){int n=f.Read(b,got,count-got);if(n==0)throw new Exception("Unexpected EOF");got+=n;}}
    static void State(string path,int k,int bound,string mode,int stage,int next,int block) {
        File.WriteAllLines(path+".tmp",new string[]{k.ToString(),bound.ToString(),mode,stage.ToString(),next.ToString(),block.ToString()});
        if(File.Exists(path))File.Replace(path+".tmp",path,null);else File.Move(path+".tmp",path);
    }
    static string StageFile(string work,int stage) {return Path.Combine(work,"stage_"+stage.ToString("D3")+".bin");}
    static BigInteger ReadInteger(BinaryReader reader) {ulong low=reader.ReadUInt64(),high=reader.ReadUInt64();return new BigInteger(low)+(new BigInteger(high)<<64);}
    static Dictionary<string,string> ReadTsv(string path) {var d=new Dictionary<string,string>();foreach(string line in File.ReadAllLines(path)){string[] s=line.Split('\t');d.Add(s[0],s[1]);}return d;}
    static void Add64(ulong[] target,int a,ulong[] source,int b) {
        ulong low=target[a]+source[b],carry=low<target[a]?1UL:0UL;
        ulong high=target[a+1]+source[b+1];if(high<target[a+1])throw new Exception("128-bit coefficient overflow");
        ulong final=high+carry;if(final<high)throw new Exception("128-bit coefficient carry overflow");target[a]=low;target[a+1]=final;
    }
    static void Add32(uint[] target,int a,uint[] source,int b) {
        ulong carry=0;for(int h=0;h<4;h++){ulong sum=(ulong)target[a+h]+source[b+h]+carry;target[a+h]=(uint)sum;carry=sum>>32;}if(carry!=0)throw new Exception("128-bit verifier overflow");
    }
    static void CheckCommitted(string output,string journal,int next,int block,byte[] bytes) {
        if(next==0){if(File.Exists(journal))File.WriteAllText(journal,"");return;}
        int expected=0;var retained=new List<string>();
        using(var f=File.OpenRead(output))foreach(string line in File.ReadAllLines(journal)) {
            string[] s=line.Split('\t');int start=int.Parse(s[0]),count=int.Parse(s[1]);if(start>=next)break;
            if(start!=expected||count<=0||count>block||start+count>next)throw new Exception("Invalid committed block journal");
            f.Position=16L*start;ReadExact(f,bytes,16*count);if(BlockHash(bytes,16*count)!=s[2])throw new Exception("Committed block checksum mismatch");
            expected+=count;retained.Add(line);
        }
        if(expected!=next)throw new Exception("Incomplete committed block journal");File.WriteAllLines(journal,retained);
    }
    public static int Main(string[] args) {
      try {
        if(args.Length<4||args.Length>6)throw new Exception("Usage: finite_disk.exe generate|verify K MAX_D OUTDIR [BLOCK_COEFFICIENTS=262144] [STOP_AFTER_BLOCKS=0]");
        string mode=args[0];bool verify=mode=="verify";if(!verify&&mode!="generate")throw new Exception("Unknown mode");
        if(!BitConverter.IsLittleEndian)throw new Exception("Little-endian host required");
        int k=int.Parse(args[1]),bound=int.Parse(args[2]),limit=checked(bound+1),total=checked(limit+1),block=args.Length>4?int.Parse(args[4]):262144,stop=args.Length>5?int.Parse(args[5]):0;
        if(block<1||block>1000000)throw new Exception("Block size must be 1..1000000");
        string dir=Path.GetFullPath(args[3]),work=Path.Combine(dir,"disk_"+mode);Directory.CreateDirectory(work);
        string state=Path.Combine(work,"state.txt");int stage=1,next=0;
        if(File.Exists(state)) {string[] s=File.ReadAllLines(state);if(int.Parse(s[0])!=k||int.Parse(s[1])!=bound||s[2]!=mode||int.Parse(s[5])!=block)throw new Exception("Resume parameters differ");stage=int.Parse(s[3]);next=int.Parse(s[4]);}
        var coins=new List<int>();for(int j=1;;j++){long x=1;for(int h=0;h<k;h++)x*=j;if(x>limit)break;coins.Add((int)x);}if(verify)coins.Reverse();
        byte[] bytes=new byte[16*block];ulong[] a64=verify?null:new ulong[2*block],b64=verify?null:new ulong[2*block];uint[] a32=verify?new uint[4*block]:null,b32=verify?new uint[4*block]:null;
        var clock=Stopwatch.StartNew();int committedThisRun=0;
        if(stage>1) {
            string previous=StageFile(work,stage-1);
            if(!File.Exists(previous)&&stage==coins.Count+1)previous=Path.Combine(dir,verify?"checker_coefficients_u128le.bin":"coefficients_u128le.bin");
            CheckCommitted(previous,Path.Combine(work,"stage_"+(stage-1).ToString("D3")+".blocks.tsv"),total,block,bytes);
        }
        for(;stage<=coins.Count;stage++) {
            int coin=coins[stage-1];string output=StageFile(work,stage),journal=Path.Combine(work,"stage_"+stage.ToString("D3")+".blocks.tsv"),prior=StageFile(work,stage-1);
            CheckCommitted(output,journal,next,block,bytes);
            using(var old=stage==1?null:new FileStream(prior,FileMode.Open,FileAccess.Read,FileShare.Read,65536))
            using(var writer=new FileStream(output,FileMode.OpenOrCreate,FileAccess.ReadWrite,FileShare.ReadWrite,65536)) {
                writer.SetLength(16L*next);writer.Position=16L*next;
                using(var source=new FileStream(output,FileMode.Open,FileAccess.Read,FileShare.ReadWrite,65536)) {
                    for(int start=next;start<total;) {
                        int count=Math.Min(block,total-start),byteCount=16*count;
                        if(old==null){Array.Clear(bytes,0,byteCount);if(start==0)bytes[0]=1;}else{old.Position=16L*start;ReadExact(old,bytes,byteCount);}
                        if(verify)Buffer.BlockCopy(bytes,0,a32,0,byteCount);else Buffer.BlockCopy(bytes,0,a64,0,byteCount);
                        int externalStart=Math.Max(0,start-coin),externalEnd=Math.Min(start,start+count-coin),externalCount=Math.Max(0,externalEnd-externalStart);
                        if(externalCount>0){source.Position=16L*externalStart;ReadExact(source,bytes,16*externalCount);if(verify)Buffer.BlockCopy(bytes,0,b32,0,16*externalCount);else Buffer.BlockCopy(bytes,0,b64,0,16*externalCount);}
                        for(int n=Math.Max(start,coin);n<start+count;n++) {
                            int sourceIndex=n-coin;
                            if(verify){if(sourceIndex>=start)Add32(a32,4*(n-start),a32,4*(sourceIndex-start));else Add32(a32,4*(n-start),b32,4*(sourceIndex-externalStart));}
                            else{if(sourceIndex>=start)Add64(a64,2*(n-start),a64,2*(sourceIndex-start));else Add64(a64,2*(n-start),b64,2*(sourceIndex-externalStart));}
                        }
                        if(verify)Buffer.BlockCopy(a32,0,bytes,0,byteCount);else Buffer.BlockCopy(a64,0,bytes,0,byteCount);
                        writer.Position=16L*start;writer.Write(bytes,0,byteCount);writer.Flush(true);
                        string hash=BlockHash(bytes,byteCount);using(var log=new StreamWriter(new FileStream(journal,FileMode.Append,FileAccess.Write,FileShare.Read))){log.WriteLine(start+"\t"+count+"\t"+hash);log.Flush();((FileStream)log.BaseStream).Flush(true);}
                        start+=count;next=start;State(state,k,bound,mode,stage,next,block);committedThisRun++;
                        if(stop>0&&committedThisRun>=stop){Console.WriteLine("CHECKPOINT_STOP mode="+mode+" stage="+stage+" next="+next);return 3;}
                    }
                }
            }
            Console.WriteLine("DISK "+mode+" stage="+stage+"/"+coins.Count+" coin="+coin+" seconds="+clock.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();
            next=0;State(state,k,bound,mode,stage+1,0,block);
            if(stage>1)File.Delete(prior); // Fixed generated file inside this run's work directory.
        }
        string final=Path.Combine(dir,verify?"checker_coefficients_u128le.bin":"coefficients_u128le.bin"),last=StageFile(work,coins.Count);
        if(File.Exists(last)){if(File.Exists(final))File.Delete(final);File.Move(last,final);}else if(!File.Exists(final))throw new Exception("Final coefficient file is missing");
        if(new FileInfo(final).Length!=16L*total)throw new Exception("Final coefficient file size differs");
        string coefficientHash=Hash(final),signFile=Path.Combine(dir,verify?"checker_signs_i8.bin":"signs_i8.bin");
        Dictionary<string,string> expected=verify?ReadTsv(Path.Combine(dir,"summary.tsv")):null;
        if(verify&&coefficientHash!=expected["coefficients_sha256"])throw new Exception("Independent coefficient digest differs");
        long negative=0,zero=0;int lastNegative=0,lastZero=0,candidate=k==4?637855:k==5?2507861:35577569;
        var witnesses=new Dictionary<int,BigInteger>();var determinants=new Dictionary<int,BigInteger>();BigInteger[] prefix=new BigInteger[Math.Min(limit,8192)+1];
        using(var reader=new BinaryReader(new BufferedStream(File.OpenRead(final),4*1024*1024)))
        using(var signs=new BufferedStream(verify?Stream.Null:File.Create(signFile),4*1024*1024))
        using(var reference=verify?(Stream)new BufferedStream(File.OpenRead(Path.Combine(dir,"signs_i8.bin")),4*1024*1024):null) {
            BigInteger prev=ReadInteger(reader),cur=ReadInteger(reader);prefix[0]=prev;prefix[1]=cur;
            for(int n=1;n<=bound;n++) {
                BigInteger after=ReadInteger(reader),det=cur*cur-prev*after;int sign=det.Sign;byte encoded=unchecked((byte)(sbyte)sign);signs.WriteByte(encoded);
                if(verify&&reference.ReadByte()!=encoded)throw new Exception("Independent exact sign comparison differs at "+n);
                if(sign<0){negative++;lastNegative=n;}else if(sign==0){zero++;lastZero=n;}
                if(n+1<prefix.Length)prefix[n+1]=after;
                if(n>=candidate-2&&n<=candidate+1)witnesses[n]=cur;
                if(n==candidate-1||n==candidate)determinants[n]=det;
                prev=cur;cur=after;if(n%10000000==0){Console.WriteLine("DISK SIGN "+n+" seconds="+clock.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();}
            }
            if(limit>=candidate-2&&limit<=candidate+1)witnesses[limit]=cur;
            if(verify&&reference.ReadByte()!=-1)throw new Exception("Extra reference signs");
        }
        // In verification mode every computed byte was compared directly with
        // the reference, so its file digest is also the exact computed-stream
        // digest. Avoid allocating a second large, identical sign file.
        string signHash=Hash(verify?Path.Combine(dir,"signs_i8.bin"):signFile);
        if(verify) {
            if(negative!=long.Parse(expected["negative_count"])||zero!=long.Parse(expected["equality_count"])||lastNegative!=int.Parse(expected["largest_negative_index"])||lastZero!=int.Parse(expected["largest_equality_index"])||signHash!=expected["signs_sha256"])throw new Exception("Independent sign summary differs");
            foreach(var item in expected){if(item.Key.StartsWith("coefficient_")){int n=int.Parse(item.Key.Substring(12));if(witnesses[n]!=BigInteger.Parse(item.Value))throw new Exception("Independent coefficient witness differs");}if(item.Key.StartsWith("determinant_")){int n=int.Parse(item.Key.Substring(12));if(determinants[n]!=BigInteger.Parse(item.Value))throw new Exception("Independent determinant witness differs");}}
            long[] divisor=new long[prefix.Length];foreach(int coin in coins)for(int n=coin;n<divisor.Length;n+=coin)divisor[n]+=coin;
            for(int n=1;n<prefix.Length;n++){BigInteger numerator=0;for(int m=1;m<=n;m++)numerator+=divisor[m]*prefix[n-m];if(numerator!=n*prefix[n])throw new Exception("Independent divisor identity differs at "+n);}
            File.WriteAllLines(Path.Combine(dir,"independent_check.tsv"),new string[]{"result\tPASS","coefficient_range\t0.."+limit,"determinant_range\t1.."+bound,"divisor_recurrence_range\t0.."+(prefix.Length-1),"coefficients_sha256\t"+coefficientHash,"signs_sha256\t"+signHash,"seconds\t"+clock.Elapsed.TotalSeconds.ToString("F3"),"runtime\t"+Environment.Version,"method\tdisk-backed reverse-order four 32-bit limbs; every BigInteger determinant; exact bytewise sign comparison"});
        } else using(var summary=new StreamWriter(Path.Combine(dir,"summary.tsv"))) {
            summary.WriteLine("k\t"+k);summary.WriteLine("max_determinant_index\t"+bound);summary.WriteLine("max_coefficient_index\t"+limit);summary.WriteLine("negative_count\t"+negative);summary.WriteLine("equality_count\t"+zero);summary.WriteLine("largest_negative_index\t"+lastNegative);summary.WriteLine("largest_equality_index\t"+lastZero);summary.WriteLine("coefficients_sha256\t"+coefficientHash);summary.WriteLine("signs_sha256\t"+signHash);summary.WriteLine("elapsed_seconds\t"+clock.Elapsed.TotalSeconds.ToString("F3"));foreach(var pair in witnesses)summary.WriteLine("coefficient_"+pair.Key+"\t"+pair.Value);foreach(var pair in determinants)summary.WriteLine("determinant_"+pair.Key+"\t"+pair.Value);
        }
        Console.WriteLine("PASS DISK "+mode+" last_negative="+lastNegative+" equality_count="+zero+" last_equality="+lastZero+" seconds="+clock.Elapsed.TotalSeconds.ToString("F3"));return 0;
      } catch(Exception e){Console.Error.WriteLine(e);return 1;}
    }
}
