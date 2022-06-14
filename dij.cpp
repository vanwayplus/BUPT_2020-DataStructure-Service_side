/*
�γ̵���ģ��
input:
��� �յ� ����ģʽ
//ģʽ1����̾��룬ֱ�Ӱ�Ȩֵ����
//ģʽ2�����ʱ�䣬Ȩֵ�������ӵ����
//ģʽ3����ͨ���ߣ����������г���
output:
��̾��� ·��
//�������ǵϽ�˹�����㷨
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
#define MaxVerNum 50   //���������Ŀֵ
#define VexType char   //������������
#define EdgeType int   //����������,����ͼʱ�ڽӾ���Գƣ���Ȩֵʱ��ʾȨֵ��û��ʱ1��0����
#define INF 0x3f3f3f3f //��Ϊ���ֵ
using namespace std;

int vn = 41, an = 201; //������������
int shaheV = 24;	   //����У���Ķ�����
string result;		   //���

//ͼ�����ݽṹ
typedef struct Graph
{
	VexType Vex[MaxVerNum][30];			 //�����
	EdgeType Edge[MaxVerNum][MaxVerNum]; //�߱�
	int vexnum, arcnum;					 //������������
} Graph;
//�Ͻ�˹�����㷨ȫ�ֱ���
bool S[MaxVerNum]; //���㼯
int D[MaxVerNum];  //��������������·��
int Pr[MaxVerNum]; //��¼ǰ��
//*********************************************������������*****************************************//
//��ʼ������ ������ͼG ���ã���ʼ��ͼ�Ķ�����ڽӾ����
void InitGraph(Graph &G)
{
	memset(G.Vex, '#', sizeof(G.Vex)); //��ʼ�������
	//��ʼ���߱�
	for (int i = 0; i < MaxVerNum; i++)
		for (int j = 0; j < MaxVerNum; j++)
			G.Edge[i][j] = INF;
	G.arcnum = G.vexnum = 0; //��ʼ��������������
}
//����㺯�� ������ͼG,����v ���ã���ͼG�в��붥��v,���ı䶥���
bool InsertNode(Graph &G, VexType v[])
{
	if (G.vexnum < MaxVerNum)
	{
		strcpy(G.Vex[G.vexnum++], v);
		return true;
	}
	return false;
}
//����ߺ��� ������ͼG,ĳ�����˵�v��w ���ã���ͼG����v,w֮�����ߣ����ı��ڽӾ���
bool InsertEdge(Graph &G, VexType *v, VexType *w, int weight)
{
	int p1, p2;						   // v,w�����±�
	p1 = p2 = -1;					   //��ʼ��
	for (int i = 0; i < G.vexnum; i++) //Ѱ�Ҷ����±�
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
	if (-1 != p1 && -1 != p2) //���������ͼ���ҵ�
	{
		G.Edge[p1][p2] = G.Edge[p2][p1] = weight; //����ͼ�ڽӾ���Գ�
		G.arcnum++;
		return true;
	}
	return false;
}

bool visited[MaxVerNum]; //���ʱ�����飬���ڱ���ʱ�ı��

//���·�� - Dijkstra�㷨 ������ͼG��Դ��v
void Dijkstra(Graph G, int v)
{
	//��ʼ��
	int n = G.vexnum; // nΪͼ�Ķ������
	for (int i = 0; i < n; i++)
	{
		S[i] = false;
		D[i] = G.Edge[v][i];
		if (D[i] < INF)
			Pr[i] = v; // v��i���ӣ�vΪǰ��
		else
			Pr[i] = -1;
	}
	S[v] = true;
	D[v] = 0;
	//��ʼ������,�����·����������S��
	for (int i = 1; i < n; i++)
	{
		int min = INF;
		int temp;
		for (int w = 0; w < n; w++)
			if (!S[w] && D[w] < min) //ĳ��tempδ����s������Ϊ��ǰ���·��
			{
				temp = w;
				min = D[w];
			}
		S[temp] = true;
		//���´�Դ����������������·�� ͨ��temp
		for (int w = 0; w < n; w++)
			if (!S[w] && D[temp] + G.Edge[temp][w] < D[w])
			{
				D[w] = D[temp] + G.Edge[temp][w];
				Pr[w] = temp;
			}
	}
}
//������·��
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
//���У��������ʱ�̱�
void SchoolBus()
{
	result = result + "\nУ��ʱ���" + "\n";
	result = result + "7\t ɳ��->������ ������->ɳ��\n";
	result = result + "11\t ɳ��->������ ������->ɳ��\n";
	result = result + "12\t ɳ��->������ ������->ɳ��\n";
	result = result + "16\t ɳ��->������ ������->ɳ��\n\n";
	result = result + "��������" + "\n";
	result = result + "670·\t ���������15����\n";
	result = result + "92·\t ���������10����\n";
	result = result + "694·\t ���������20����\n";
}

//����ͼ����ʵ�ֺ��� ������ͼG  InsertNode ���ã�����ͼ
void CreateGraph(Graph &G, int mode)
{
	ifstream infile, infile1;
	infile.open("graph.txt"); //���ļ����������ļ���������
	infile1.open("node.txt");
	assert(infile.is_open()); //��ʧ��,�����������Ϣ,����ֹ��������
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
			continue; //�����
		}
		else
		{
			cout << "error";
			break;
		}
	}
	// cout << "���������бߣ�ÿ����������ӵ��������㼰Ȩֵ��:" << endl;
	for (int j = 0; j < an; j++)
	{
		int weight;

		infile >> v;
		infile >> w;
		infile >> wei;
		weight = atoi(wei.c_str()); // stringתint
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
			continue; //�����
		}
		else
		{
			cout << "�������" << endl;
			break;
		}
	}
	infile.close();	 //�ر��ļ�������
	infile1.close(); //�ر��ļ�������
}

//������洢�����result
void print(Graph &G, int i)
{
	result = result + to_string(D[i]) + "\n";
	Path(G, i);
	result += G.Vex[i];
	result += "\n";
	// ofile.close();
}

//����У�����õϽ�˹����
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

	// cout << "Ŀ���"
	// 	 << "\t"
	// 	 << "���·��ֵ"
	// 	 << "\t"
	// 	 << "���·��" << endl;

	//����յ���ͬһУ��
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
	// ����յ��ڲ�ͬУ��
	else
	{
		for (int i = 0; i < G.vexnum; i++)
		{
			if (!strcmp(G.Vex[i], "����"))
				w = i;
			if (!strcmp(G.Vex[i], "����"))
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
			//��ʵ�֣�У�����ܣ���ϵͳʱ��ҹ���
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


//������
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
	infile.open("xxx.txt");	  //�޸��ļ���
	assert(infile.is_open()); //��ʧ��,�����������Ϣ,����ֹ��������

	char start[30], end[30]; //�ӿ�
	int mode;				 //�ӿ�
	infile >> start;
	infile >> end;
	infile >> mode;

	string ans;					   //���
	ans = graph(start, end, mode); //����������
	ofstream ofile;
	ofile.open("xxxx.txt", ios::out);
	ofile << ans;
	ofile.close();
	cout << ans;
	system("pause");
	return 0;
}