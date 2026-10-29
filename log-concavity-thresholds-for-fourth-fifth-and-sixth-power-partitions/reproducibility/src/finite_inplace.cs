// One-file, bounded-memory independent coefficient reconstruction.
// Parts are processed in descending order, using four checked 32-bit limbs.
// An undo block is persisted before every in-place update; the state marker
// commits that block only after coefficient bytes and the checksum log flush.
using System;
using System.IO;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

public static class FiniteInplace {
    static string Hex(byte[] b){return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
    static string Digest(byte[] b,int n){using(var h=SHA256.Create())return Hex(h.ComputeHash(b,0,n));}
    static void Read(Stream f,byte[] b,int n){int p=0;while(p<n){int r=f.Read(b,p,n-p);if(r==0)throw new Exception("Unexpected EOF");p+=r;}}
    static void Text(string path,string[] lines){
        string temporary=path+".tmp."+Guid.NewGuid().ToString("N");
        using(var f=new FileStream(temporary,FileMode.CreateNew,FileAccess.Write,FileShare.Read))using(var w=new StreamWriter(f)){foreach(string line in lines)w.WriteLine(line);w.Flush();f.Flush(true);}
        for(int attempt=0;;attempt++)try{if(File.Exists(path))File.Replace(temporary,path,null);else File.Move(temporary,path);return;}catch(IOException){if(attempt>=99)throw;Thread.Sleep(50);}
    }
    static void State(string path,int k,int bound,int stage,int next,int block){Text(path,new string[]{k.ToString(),bound.ToString(),stage.ToString(),next.ToString(),block.ToString()});}
    static string Log(string work,int stage){return Path.Combine(work,"stage_"+stage.ToString("D3")+".blocks.tsv");}
    static void Append(string path,int start,int count,string hash){using(var f=new FileStream(path,FileMode.Append,FileAccess.Write,FileShare.Read))using(var w=new StreamWriter(f)){w.WriteLine(start+"\t"+count+"\t"+hash);w.Flush();f.Flush(true);}}
    static Dictionary<int,string[]> Entries(string path){var d=new Dictionary<int,string[]>();if(File.Exists(path))foreach(string line in File.ReadAllLines(path)){string[] s=line.Split('\t');d[int.Parse(s[0])]=s;}return d;}
    static void VerifyFile(string path,string work,int stage,int next,int total,int block,byte[] bytes){
        var old=Entries(Log(work,stage-1));var updated=Entries(Log(work,stage));
        using(var f=File.OpenRead(path)){if(f.Length!=16L*total)throw new Exception("Coefficient file length mismatch");for(int start=0;start<total;start+=block){int n=Math.Min(block,total-start);var map=start<next?updated:old;if(!map.ContainsKey(start)||int.Parse(map[start][1])!=n)throw new Exception("Missing block checksum "+start);Read(f,bytes,16*n);if(Digest(bytes,16*n)!=map[start][2])throw new Exception("Committed coefficient block checksum mismatch at "+start);}}
        var keep=new List<string>();foreach(var pair in updated)if(pair.Key<next)keep.Add(string.Join("\t",pair.Value));keep.Sort(delegate(string a,string b){return int.Parse(a.Split('\t')[0]).CompareTo(int.Parse(b.Split('\t')[0]));});File.WriteAllLines(Log(work,stage),keep);
    }
    public static int Main(string[] args){
      try{
        if(args.Length<3||args.Length>5)throw new Exception("Usage: finite_inplace.exe K BOUND CASEDIR [BLOCK=262144] [STOP_AFTER_BLOCKS=0]");
        int k=int.Parse(args[0]),bound=int.Parse(args[1]),limit=checked(bound+1),total=checked(limit+1),block=args.Length>3?int.Parse(args[3]):262144,stop=args.Length>4?int.Parse(args[4]):0;
        if(!BitConverter.IsLittleEndian||block<1||block>1000000)throw new Exception("Unsupported endian or block size");
        string dir=Path.GetFullPath(args[2]),work=Path.Combine(dir,"disk_verify_inplace");Directory.CreateDirectory(work);
        string state=Path.Combine(work,"state.txt"),data=Path.Combine(dir,"checker_coefficients_u128le.bin"),undo=Path.Combine(work,"undo.bin"),intent=Path.Combine(work,"intent.txt");
        byte[] bytes=new byte[16*block];uint[] values=new uint[4*block],source=new uint[4*block];int stage=1,next=0;
        var coins=new List<int>();for(int j=1;;j++){long v=1;for(int h=0;h<k;h++)v*=j;if(v>limit)break;coins.Add((int)v);}coins.Reverse();
        if(!File.Exists(state)){
            if(File.Exists(data))throw new Exception("Existing coefficient file without in-place state; migrate first");
            using(var f=new FileStream(data,FileMode.CreateNew,FileAccess.Write,FileShare.Read,65536))for(int start=0;start<total;start+=block){int count=Math.Min(block,total-start);Array.Clear(bytes,0,16*count);if(start==0)bytes[0]=1;f.Write(bytes,0,16*count);Append(Log(work,0),start,count,Digest(bytes,16*count));f.Flush(true);}State(state,k,bound,1,0,block);
        }
        string[] saved=File.ReadAllLines(state);if(int.Parse(saved[0])!=k||int.Parse(saved[1])!=bound||int.Parse(saved[4])!=block)throw new Exception("In-place resume parameters differ");stage=int.Parse(saved[2]);next=int.Parse(saved[3]);
        if(File.Exists(intent)){
            string[] s=File.ReadAllLines(intent);int pendingStage=int.Parse(s[0]),start=int.Parse(s[1]),count=int.Parse(s[2]);
            if(stage==pendingStage&&next==start){using(var f=File.OpenRead(undo))Read(f,bytes,16*count);if(Digest(bytes,16*count)!=s[3])throw new Exception("Undo checksum mismatch");using(var f=new FileStream(data,FileMode.Open,FileAccess.Write,FileShare.Read)){f.Position=16L*start;f.Write(bytes,0,16*count);f.Flush(true);}}
            else if((stage==pendingStage&&next>=start+count)||stage>pendingStage){using(var f=File.OpenRead(data)){f.Position=16L*start;Read(f,bytes,16*count);}if(Digest(bytes,16*count)!=s[4])throw new Exception("Committed pending block mismatch");}
            else throw new Exception("Inconsistent pending block state");
            File.Delete(intent);File.Delete(undo);
        }
        VerifyFile(data,work,stage,next,total,block,bytes);var timer=Stopwatch.StartNew();int done=0;
        using(var file=new FileStream(data,FileMode.Open,FileAccess.ReadWrite,FileShare.Read,65536))for(;stage<=coins.Count;stage++){
            int coin=coins[stage-1];
            for(int start=next;start<total;){
                int count=Math.Min(block,total-start),byteCount=16*count;file.Position=16L*start;Read(file,bytes,byteCount);string before=Digest(bytes,byteCount);Buffer.BlockCopy(bytes,0,values,0,byteCount);
                using(var backup=new FileStream(undo,FileMode.Create,FileAccess.Write,FileShare.Read)){backup.Write(bytes,0,byteCount);backup.Flush(true);}
                int externalStart=Math.Max(0,start-coin),externalEnd=Math.Min(start,start+count-coin),externalCount=Math.Max(0,externalEnd-externalStart);
                if(externalCount>0){file.Position=16L*externalStart;Read(file,bytes,16*externalCount);Buffer.BlockCopy(bytes,0,source,0,16*externalCount);}
                for(int n=Math.Max(start,coin);n<start+count;n++){int from=n-coin,a=4*(n-start),b=4*(from>=start?from-start:from-externalStart);uint[] src=from>=start?values:source;ulong carry=0;for(int h=0;h<4;h++){ulong sum=(ulong)values[a+h]+src[b+h]+carry;values[a+h]=(uint)sum;carry=sum>>32;}if(carry!=0)throw new Exception("128-bit overflow in independent in-place reconstruction");}
                Buffer.BlockCopy(values,0,bytes,0,byteCount);string after=Digest(bytes,byteCount);Text(intent,new string[]{stage.ToString(),start.ToString(),count.ToString(),before,after});
                file.Position=16L*start;file.Write(bytes,0,byteCount);file.Flush(true);Append(Log(work,stage),start,count,after);
                start+=count;next=start;State(state,k,bound,stage,next,block);File.Delete(intent);File.Delete(undo);done++;
                if(stop>0&&done>=stop){Console.WriteLine("INPLACE_CHECKPOINT stage="+stage+" next="+next);return 3;}
            }
            next=0;State(state,k,bound,stage+1,0,block);Console.WriteLine("INPLACE stage="+stage+"/"+coins.Count+" coin="+coin+" seconds="+timer.Elapsed.TotalSeconds.ToString("F3"));Console.Out.Flush();
        }
        // Produce the compatibility checkpoint for the already independent
        // BigInteger determinant/witness/divisor-prefix checker in finite_disk.
        string compatibility=Path.Combine(dir,"disk_verify");Directory.CreateDirectory(compatibility);File.Copy(Log(work,coins.Count),Log(compatibility,coins.Count),true);
        Text(Path.Combine(compatibility,"state.txt"),new string[]{k.ToString(),bound.ToString(),"verify",(coins.Count+1).ToString(),"0",block.ToString()});
        Console.WriteLine("INPLACE COEFFICIENTS COMPLETE; run finite_disk.exe verify for all exact determinants");return 0;
      }catch(Exception e){Console.Error.WriteLine(e);return 1;}
    }
}
