using System;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;

// Exact bounded search. Apéry residues and factorization support graphs use integers only.
public class SearchSemigroups {
  static int[] g=new int[4], w=new int[20000];
  static bool[] used=new bool[20000];
  static long examined=0, semigroups=0, ng=0, nonas=0;
  static bool counterexampleFound=false;
  static Dictionary<int,long> histogram=new Dictionary<int,long>();
  static StreamWriter result;
  static int Gcd(int a,int b){while(b!=0){int t=a%b;a=b;b=t;}return a;}
  static bool Member(int n){return n>=0 && w[n%g[0]]<=n;}
  static string Arr(List<int> a){return "["+string.Join(",",a.ConvertAll(x=>x.ToString()).ToArray())+"]";}
  static int Root(int[] p,int i){while(p[i]!=i)i=p[i];return i;}
  static void Evaluate(){
    examined++;
    int a=g[0]; if(Gcd(Gcd(Gcd(a,g[1]),g[2]),g[3])!=1)return;
    // Dijkstra in the residue graph, using all four generators.
    for(int r=0;r<a;r++){w[r]=int.MaxValue/4;used[r]=false;}w[0]=0;
    for(int k=0;k<a;k++){
      int u=-1; for(int r=0;r<a;r++)if(!used[r]&&(u<0||w[r]<w[u]))u=r;
      used[u]=true;
      for(int i=1;i<4;i++){int v=(u+g[i])%a;if(w[v]>w[u]+g[i])w[v]=w[u]+g[i];}
    }
    // Minimality: a generator has another positive-generator summand exactly if redundant.
    for(int i=1;i<4;i++)for(int j=0;j<i;j++)if(Member(g[i]-g[j]))return;
    semigroups++;
    List<int> pf=new List<int>(); int F=0;
    for(int r=0;r<a;r++){
      int f=w[r]-a;if(f>F)F=f;
      bool ok=true;for(int i=1;i<4;i++)if(!Member(f+g[i])){ok=false;break;}
      if(ok)pf.Add(f);
    }
    pf.Sort();
    List<int> nv=new List<int>();
    for(int i=0;i<4;i++){
      bool found=false;
      foreach(int p in pf){bool ok=true;foreach(int q in pf)if(!Member(g[i]+p-q)){ok=false;break;}
        if(ok){nv.Add(p);found=true;break;}}
      if(!found)return;
    }
    ng++;
    bool almost=true;
    foreach(int q in pf)if(!Member(F+a-q)){almost=false;break;}
    // Full almost symmetric test (equivalently the NG vector can be constantly F).
    if(almost)for(int i=1;i<4;i++)foreach(int q in pf)if(!Member(F+g[i]-q)){almost=false;break;}
    if(almost)return;
    nonas++;
    int rho=0;List<string> bs=new List<string>();
    // For n>F+g[2]+g[3], every pair of vertices is joined, hence no Betti degree.
    for(int n=2*a;n<=F+g[2]+g[3];n++){
      int[] p={0,1,2,3};bool[] active=new bool[4];int components=0;
      for(int i=0;i<4;i++)if(Member(n-g[i])){active[i]=true;components++;}
      if(components<2)continue;
      for(int i=0;i<4;i++)if(active[i])for(int j=i+1;j<4;j++)if(active[j]&&Member(n-g[i]-g[j])){
        int ri=Root(p,i),rj=Root(p,j);if(ri!=rj){p[rj]=ri;components--;}}
      if(components>1){rho+=components-1;bs.Add("["+n+","+components+"]");}
    }
    if(!histogram.ContainsKey(rho))histogram[rho]=0;histogram[rho]++;
    string row="{\"generators\":["+string.Join(",",g)+"],\"F\":"+F+",\"PF\":"+Arr(pf)+",\"NG_vector\":"+Arr(nv)+",\"rho\":"+rho+",\"betti_degree_components\":["+string.Join(",",bs.ToArray())+"]}";
    result.WriteLine(row);result.Flush();
    if(rho!=5&&rho!=6){Console.WriteLine("COUNTEREXAMPLE "+row);counterexampleFound=true;}
  }
  public static void Main(string[] args){
    int max=int.Parse(args[0]);result=new StreamWriter(args[1]);Stopwatch sw=Stopwatch.StartNew();
    try {
      for(int d=5;d<=max&&!counterexampleFound;d++){
        g[3]=d;
        for(int c=4;c<d&&!counterexampleFound;c++){g[2]=c;
          for(int b=3;b<c&&!counterexampleFound;b++){g[1]=b;
            for(int a=4;a<b&&!counterexampleFound;a++){g[0]=a;Evaluate();}}}
        if(d%10==0)Console.WriteLine("max="+d+" tuples="+examined+" minimal="+semigroups+" NG="+ng+" nonAS="+nonas+" seconds="+sw.Elapsed.TotalSeconds.ToString("F2"));
      }
    } finally {result.Close();}
    Console.WriteLine("SUMMARY requested_max="+max+" last_max_generator="+g[3]+" stopped_on_counterexample="+counterexampleFound+" tuples="+examined+" minimal="+semigroups+" NG="+ng+" nonAS="+nonas+" seconds="+sw.Elapsed.TotalSeconds.ToString("F2"));
    foreach(var kv in histogram)Console.WriteLine("rho="+kv.Key+" count="+kv.Value);
  }
}
