/*
课程导航模块
input:
起点 终点 导航模式
//模式1：最短距离，直接按权值搜索
//模式2：最短时间，权值乘上随机拥挤度
//模式3：交通工具，仅保留自行车道
output:
最短距离 路径
//本质上是迪杰斯特拉算法
*/
#include <cstring>
#include <string>
#include <set>
#include <list>
#include <queue>
#include <vector>
#include <map>
#include <iterator>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include "fstream"
//#include <conio.h>
#include <assert.h>
#define MaxVerNum 50   //顶点最大数目值
#define VexType char   //顶点数据类型
#define EdgeType int   //边数据类型,无向图时邻接矩阵对称，有权值时表示权值，没有时1连0不连
#define INF 0x3f3f3f3f //作为最大值
using namespace std;

int vn = 41, an = 201; //顶点数，边数
int shaheV = 24;	   //两个校区的顶点数
string result;		   //结果

//图的数据结构
typedef struct Graph
{
	VexType Vex[MaxVerNum][30];			 //顶点表
	EdgeType Edge[MaxVerNum][MaxVerNum]; //边表
	int vexnum, arcnum;					 //顶点数、边数
} Graph;
//迪杰斯特拉算法全局变量
bool S[MaxVerNum]; //顶点集
int D[MaxVerNum];  //到各个顶点的最短路径
int Pr[MaxVerNum]; //记录前驱
//*********************************************基本操作函数*****************************************//
//初始化函数 参数：图G 作用：初始化图的顶点表，邻接矩阵等
void InitGraph(Graph &G)
{
	memset(G.Vex, '#', sizeof(G.Vex)); //初始化顶点表
	//初始化边表
	for (int i = 0; i < MaxVerNum; i++)
		for (int j = 0; j < MaxVerNum; j++)
			G.Edge[i][j] = INF;
	G.arcnum = G.vexnum = 0; //初始化顶点数、边数
}
//插入点函数 参数：图G,顶点v 作用：在图G中插入顶点v,即改变顶点表
bool InsertNode(Graph &G, VexType v[])
{
	if (G.vexnum < MaxVerNum)
	{
		strcpy(G.Vex[G.vexnum++], v);
		return true;
	}
	return false;
}
//插入边函数 参数：图G,某边两端点v和w 作用：在图G两点v,w之间加入边，即改变邻接矩阵
bool InsertEdge(Graph &G, VexType *v, VexType *w, int weight)
{
	int p1, p2;						   // v,w两点下标
	p1 = p2 = -1;					   //初始化
	for (int i = 0; i < G.vexnum; i++) //寻找顶点下标
	{
		if (!strcmp(G.Vex[i], v))
		{
			p1 = i;
		}

		if (!strcmp(G.Vex[i], w))
		{
			p2 = i;
		}
	}
	if (-1 != p1 && -1 != p2) //两点均可在图中找到
	{
		G.Edge[p1][p2] = G.Edge[p2][p1] = weight; //无向图邻接矩阵对称
		G.arcnum++;
		return true;
	}
	return false;
}

bool visited[MaxVerNum]; //访问标记数组，用于遍历时的标记

//最短路径 - Dijkstra算法 参数：图G、源点v
void Dijkstra(Graph G, int v)
{
	//初始化
	int n = G.vexnum; // n为图的顶点个数
	for (int i = 0; i < n; i++)
	{
		S[i] = false;
		D[i] = G.Edge[v][i];
		if (D[i] < INF)
			Pr[i] = v; // v与i连接，v为前驱
		else
			Pr[i] = -1;
	}
	S[v] = true;
	D[v] = 0;
	//初始化结束,求最短路径，并加入S集
	for (int i = 1; i < n; i++)
	{
		int min = INF;
		int temp;
		for (int w = 0; w < n; w++)
			if (!S[w] && D[w] < min) //某点temp未加入s集，且为当前最短路径
			{
				temp = w;
				min = D[w];
			}
		S[temp] = true;
		//更新从源点出发至其余点的最短路径 通过temp
		for (int w = 0; w < n; w++)
			if (!S[w] && D[temp] + G.Edge[temp][w] < D[w])
			{
				D[w] = D[temp] + G.Edge[temp][w];
				Pr[w] = temp;
			}
	}
}
//输出最短路径
void Path(Graph G, int v)
{
	if (Pr[v] == -1)
		return;
	Path(G, Pr[v]);
	result += G.Vex[Pr[v]];
	result += "\n";
	// result += "->";
	// cout << G.Vex[Pr[v]] << "->";
}
//输出校车公交车时刻表
void SchoolBus()
{
	result = result + "\n校车时间表：" + "\n";
	result = result + "7\t 沙河->西土城 西土城->沙河\n";
	result = result + "11\t 沙河->西土城 西土城->沙河\n";
	result = result + "12\t 沙河->西土城 西土城->沙河\n";
	result = result + "16\t 沙河->西土城 西土城->沙河\n\n";
	result = result + "公交车表：" + "\n";
	result = result + "670路\t 发车间隔：15分钟\n";
	result = result + "92路\t 发车间隔：10分钟\n";
	result = result + "694路\t 发车间隔：20分钟\n";
}

//创建图功能实现函数 参数：图G  InsertNode 作用：创建图
void CreateGraph(Graph &G, int mode)
{
	ifstream infile, infile1;
	infile.open("graph.txt"); //将文件流对象与文件连接起来
	infile1.open("node.txt");
	assert(infile.is_open()); //若失败,则输出错误消息,并终止程序运行
	assert(infile1.is_open());

	VexType v[30], w[30], buf[30];
	string wei, nod;
	char *n = buf;
	bool isBikeRoad;

	for (int i = 0; i < vn; i++)
	{
		getline(infile1, nod);
		strcpy(n, nod.c_str());
		if (InsertNode(G, n))
		{
			continue; //插入点
		}
		else
		{
			cout << "error";
			break;
		}
	}
	// cout << "请输入所有边（每行输入边连接的两个顶点及权值）:" << endl;
	for (int j = 0; j < an; j++)
	{
		int weight;

		infile >> v;
		infile >> w;
		infile >> wei;
		weight = atoi(wei.c_str()); // string转int
		infile >> isBikeRoad;

		if (mode == 2)
		{
			weight *= rand() / (RAND_MAX + 1.0);
		}
		else if (mode == 3)
		{
			if (!isBikeRoad)
			{
				continue;
			}
		}

		if (InsertEdge(G, v, w, weight))
		{
			continue; //插入边
		}
		else
		{
			cout << "输入错误！" << endl;
			break;
		}
	}
	infile.close();	 //关闭文件输入流
	infile1.close(); //关闭文件输入流
}

//将结果存储进结果result
void print(Graph &G, int i)
{
	result = result + to_string(D[i]) + "\n";
	Path(G, i);
	result += G.Vex[i];
	result += "\n";
	// ofile.close();
}

//根据校区调用迪杰斯特拉
void Shortest_Dijkstra(Graph &G, char *vname, char *des)
{
	int v = -1, v1 = -1;
	int w = -1, e = -1;

	for (int i = 0; i < G.vexnum; i++)
	{
		if (!strcmp(G.Vex[i], vname))
			v = i;
		if (!strcmp(G.Vex[i], des))
			v1 = i;
	}

	// cout << "目标点"
	// 	 << "\t"
	// 	 << "最短路径值"
	// 	 << "\t"
	// 	 << "最短路径" << endl;

	//起点终点在同一校区
	if ((0 <= v && v < shaheV) && (0 <= v1 && v1 < shaheV) || (shaheV <= v && v < vn) && (shaheV <= v1 && v1 < vn))
	{
		Dijkstra(G, v);
		for (int i = 0; i < G.vexnum; i++)
		{
			if (i == v1)
			{
				print(G, i);
			}
		}
	}
	// 起点终点在不同校区
	else
	{
		for (int i = 0; i < G.vexnum; i++)
		{
			if (!strcmp(G.Vex[i], "西门"))
				w = i;
			if (!strcmp(G.Vex[i], "东门"))
				e = i;
		}
		if (v < v1)
		{
			Dijkstra(G, v);
			for (int i = 0; i < G.vexnum; i++)
			{
				if (i == w)
				{
					print(G, i);
				}
			}
			Dijkstra(G, e);
			for (int i = 0; i < G.vexnum; i++)
			{
				if (i == v1)
				{
					print(G, i);
				}
			}
			//待实现：校车功能（和系统时间挂钩）
			SchoolBus();
		}
		else if (v > v1)
		{
			Dijkstra(G, v);
			for (int i = 0; i < G.vexnum; i++)
			{
				if (i == e)
				{
					print(G, i);
				}
			}
			Dijkstra(G, w);
			for (int i = 0; i < G.vexnum; i++)
			{
				if (i == v1)
				{
					print(G, i);
				}
			}
		}
	}
}


//主函数
string graph(char *start, char *end, int mode)
{
	Graph G;
	InitGraph(G);
	CreateGraph(G, mode);
	Shortest_Dijkstra(G, start, end);
	return result;
}

int main()
{
	ifstream infile;
	infile.open("xxx.txt");	  //修改文件名
	assert(infile.is_open()); //若失败,则输出错误消息,并终止程序运行

	char start[30], end[30]; //接口
	int mode;				 //接口
	infile >> start;
	infile >> end;
	infile >> mode;

	string ans;					   //结果
	ans = graph(start, end, mode); //调用主函数
	ofstream ofile;
	ofile.open("xxxx.txt", ios::out);
	ofile << ans;
	ofile.close();
	cout << ans;
	system("pause");
	return 0;
}