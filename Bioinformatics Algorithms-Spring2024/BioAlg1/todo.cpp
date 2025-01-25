/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include<iostream>
#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<cmath>
#include<algorithm>
#include<queue>
#include<vector>
using namespace std;
#define MAX 200
#define MAXL 200000
#define INF 1000000000
struct Line
{
    int v,next,w,fb,fy;
}e[MAXL];
int h[MAX],cnt=1,cost,ff;
int tot[MAX],need[MAX][MAX],have[MAX][MAX],Cost[MAX][MAX][MAX];
int pe[MAX],pr[MAX],Ans;
inline void Add(int u,int v,int w,int fy)
{
    e[cnt]=(Line){v,h[u],w,cnt+1,fy};
    h[u]=cnt++;
    e[cnt]=(Line){u,h[v],0,cnt-1,-fy};
    h[v]=cnt++;
}
int dis[MAX],S,T,N,M,K;
 
bool vis[MAX];
bool SPFA()
{
    memset(dis,63,sizeof(dis));
    dis[S]=0;
    queue<int> Q;while(!Q.empty())Q.pop();
    Q.push(S);
    memset(vis,0,sizeof(vis));
    while(!Q.empty())
    {
        int u=Q.front();Q.pop();
        vis[u]=false;
        for(int i=h[u];i;i=e[i].next)
        {
            int f=dis[u]+e[i].fy,v=e[i].v;
            if(e[i].w&&dis[v]>f)
            {
                dis[v]=f;
                pe[v]=i;
                pr[v]=u;
                if(!vis[v])
                {
                    vis[v]=true;
                    Q.push(v);
                }
            }
        }
    }
    if (dis [T] == dis [T + 1]) return false; // augmented failure
    int re=INF;
    for(int v=T;v!=S;v=pr[v])
                 re = min (re, e[pe [v]].w); // calculate the maximum flow augmentation
    for(int v=T;v!=S;v=pr[v])
    {
        e[pe[v]].w-=re;
        e[e[pe[v]].fb].w+=re;
    }
    ff+=re;
    cost+=re*dis[T];
    return true;
}
int main()
{
    while(233)
    {
        cin>>N>>M>>K;
        if(N==0&&M==0&&K==0)break;
        memset(tot,0,sizeof(tot));
        for(int i=1;i<=N;++i)
        {
            for(int j=1;j<=K;++j)
            {
                cin>>need[i][j];
                tot[j]+=need[i][j];
            }
        }
        for(int i=1;i<=M;++i)
        {
            for(int j=1;j<=K;++j) 
            {
                cin>>have[i][j];
                tot[j]-=have[i][j];
            }
        }
        for(int i=1;i<=K;++i)
        {
            for(int j=1;j<=N;++j)
                for(int k=1;k<=M;++k)
                    cin>>Cost[i][j][k];
        }
        S=0;T=N+M+1;
        bool fl=true;
        for(int k=1;k<=K;++k)
                         if (tot [k]> 0) // needs to provide more than
            {
                fl=false;
                break;
            }
        if(!fl)
        {
            fl=true;
            printf("%d\n",-1);
            continue;
        }
        Ans=0;
                 for (int k = 1; k <= K; ++ k) // K times cost flow
        {
            cnt=1;
            memset(h,0,sizeof(h));
            for(int j=1;j<=M;++j)
            {
                Add(S,j,have[j][k],0);
                for(int i=1;i<=N;++i)
                    Add(j,i+M,have[j][k],Cost[k][i][j]);   
            }
            for(int i=1;i<=N;++i)
                Add(i+M,T,need[i][k],0);
            cost=ff=0;
            while(SPFA());
            Ans+=cost;
        }
        printf("%d\n",Ans);
    }
    return 0;
}
