
#include<stdio.h>
#include<string.h>  
#include<math.h>  
  
#include<map>   
//#include<set>
#include<deque>  
#include<queue>  
#include<stack>  
#include<bitset> 
#include<string>  
#include<fstream>
#include<iostream>  
#include<algorithm>  
using namespace std;  

#define ll long long  
#define INF 0x3f3f3f3f  
#define mod 998244353
//#define max(a,b) (a)>(b)?(a):(b)
//#define min(a,b) (a)<(b)?(a):(b) 
#define clean(a,b) memset(a,b,sizeof(a))// 水印 
//std::ios::sync_with_stdio(false);



struct dots{
	int x,y;
}dots[110],dott[110];
struct node{
	int v,w,cost,nxt;
	node(int _v=0,int _w=0,int _cost=0,int _nxt=0):
    v(_v),w(_w),cost(_cost),nxt(_nxt){}
}edge[100010<<1];
int head[100010],ecnt;
int dis[100010],flow[100010],pre[100010],last[100010];
//	最小花费	流量			前驱		这条边 
int vis[100010];
int maxw,mincost;
int n,m,k,s,t;
void intt()
{
	clean(head,-1);
	clean(last,0);
	clean(pre,-1);
	ecnt=0;
	maxw=0,mincost=0;
}
void add(int u,int v,int w,int cost)
{
	edge[ecnt]=node(v,w,cost,head[u]);
	head[u]=ecnt++;
	edge[ecnt]=node(u,0,-cost,head[v]);
	head[v]=ecnt++;
}
/*---上面的是板子，不用动---*/

bool spfa()
{
	clean(dis,INF);
	clean(flow,INF);
	clean(vis,0);
	queue<int> que;
	que.push(s);
	vis[s]=1;
	dis[s]=0;
	pre[t]=-1;
	while(que.size())
	{
		int u=que.front();
		que.pop();
		vis[u]=0;
		for(int i=head[u];i+1;i=edge[i].nxt)
		{
			int temp=edge[i].v;
			if(dis[temp]>dis[u]+edge[i].cost&&edge[i].w>0)
			{
				dis[temp]=dis[u]+edge[i].cost;
				pre[temp]=u;
				last[temp]=i;
				flow[temp]=min(edge[i].w,flow[u]);
				if(vis[temp]==0)
				{
					vis[temp]=1;
					que.push(temp);
				}
			}
		}
	}
	return pre[t]!=-1;
}

void MCMF()
{
	while(spfa())
	{
		int u=t;
		maxw+=flow[t];//最大流 
		mincost+=dis[t]*flow[t];//最小费用 
		while(u!=s)
		{
			edge[last[u]].w-=flow[t];
			edge[last[u]^1].w+=flow[t];
			u=pre[u];
		}
	}
	//cout<<mincost<<endl;
	//cout<<maxw<<" "<<mincost<<endl;
}

int shop[55][55];//最多50个商店的50种需求 
int ware[55][55];//最多50个仓库的50种商品 
int cost[55][55][55];//50种商品别从50个仓库运送到50个商店的价格 
int rela[55][2];
int main()
{
	std::ios::sync_with_stdio(false);
	while(cin>>n>>m>>k&&n!=0)
	{
		int ans=0;
		clean(rela,0);
		clean(cost,0);
		clean(shop,0);
		clean(ware,0);
		for(int i=1;i<=n;++i)//第i个商店 
			for(int j=1;j<=k;++j)//第j种需求 
			{
				cin>>shop[i][j];
				rela[j][0]+=shop[i][j];
			}
		for(int i=1;i<=m;++i)//第i个仓库 
			for(int j=1;j<=k;++j)//第j种商品的 库存 
			{
				cin>>ware[i][j];
				rela[j][1]+=ware[i][j];
			}
		for(int i=1;i<=k;++i)//运送第i种货物
			for(int j=1;j<=n;++j)//运到第j个商店 
				for(int z=1;z<=m;++z)//从第z个仓库 
					cin>>cost[i][z][j];
		int f=0;
		for(int i=1;i<=k;++i)
			if(rela[i][0]>rela[i][1])//供不应求 
				f=1;
		if(f)
		{
			cout<<-1<<endl;
			continue;
		}
		for(int z=1;z<=k;++z)
		{
			intt();
			s=0,t=201;
			for(int i=1;i<=n;++i)//对于商店 
				add(s,i,shop[i][z],0);
			for(int i=1;i<=m;++i)//对于仓库 
				add(i+50,t,ware[i][z],0);
			for(int i=1;i<=n;++i)
			{
				for(int j=1;j<=m;++j)
				{
					add(i,j+50,INF,cost[z][j][i]);
				}
			}
			MCMF();
			if(maxw<rela[z][0])//只要有一个不符合要求，全部就都不符合要求 
			{
				cout<<-1<<endl;
				break;
			}
			ans+=mincost;
		}
		if(f==0)
			cout<<ans<<endl;
	}
}
