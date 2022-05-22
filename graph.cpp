#include <vector>
#include <string>
#include <tuple>
#include <unordered_map>
#include<cmath>
#include <queue>
#include <memory>
#include <algorithm>
#include <random>

using namespace std;

struct Vector2D
{
    int x;
    int y;
    
    Vector2D(int _x, int _y) : x(_x), y(_y)
    {}
    
    Vector2D operator+(Vector2D b) const
    {
        return {x + b.x, y + b.y};
    }
};

struct Node
{
    unsigned long long id;
    
    Node(unsigned long long _id) : id(_id)
    {}
    
    virtual bool getType() const = 0;
};

struct MapNode : public Node
{
    int mapId;
    std::string name;
    Vector2D position;
    int speed = 0;
    
    MapNode(unsigned long long _id, int _mapId, std::string _name, Vector2D _position) :
            Node(_id), mapId(_mapId), name(std::move(_name)), position(_position)
    {}
    
    bool getType() const override
    { return true; }
};

struct PortNode : public Node
{
    int level;
    unsigned long long stMapId;
    unsigned long long edMapId;
    unsigned long long stNodeId;
    unsigned long long edNodeId;
    
    PortNode(unsigned long long _id, int _level, unsigned long long _stMapId, unsigned long long _edMapId,
             unsigned long long _stNodeId, unsigned long long _edNodeId) :
            Node(_id), level(_level), stMapId(_stMapId), edMapId(_edMapId), stNodeId(_stNodeId), edNodeId(_edNodeId)
    {}
    
    bool getType() const override
    { return false; }
};

struct EdgeNode
{
    unsigned long long id;
    int st;
    int ed;
    int length;
    int speed;
    int level;
};

typedef std::vector<const Node *> Path;

class Graph
{
private:
    int vertex_count = 0;
    std::vector<MapNode> nodes;
    std::vector<std::vector<EdgeNode>> edges;
    std::vector<PortNode> ports;
    double scale;
    int lastTime = -10000; ///< 涓婁竴娆￠殢鏈洪€熷害鐨勬椂闂�
    int avgSpeed = 340;

public:
    struct EdgeData
    {
        unsigned long long id;
        int st;
        int ed;
        int length;
        int level;
    };
    
    Graph() = default;
    
    void loadMap(int nodeNum, const std::vector<MapNode> &nodeData, const std::vector<EdgeData> &edgeData);
    
    void loadPort(const std::vector<PortNode> &portData, double scale);
    
    const std::vector<MapNode> &getNodes() const
    { return nodes; }
    
    const std::vector<std::vector<EdgeNode>> &getEdges() const
    { return edges; }
    
    const std::vector<PortNode> &getPorts() const
    { return ports; }
    
    ~Graph() = default;
    
    int getDis(const Vector2D &u, const Vector2D &v) const
    {
        return sqrt((u.x - v.x) * (u.x - v.x) + (u.y - v.y) * (u.y - v.y)) * 100 * scale;
    }
    
    void setSpeed(int time);
    
    int dijkstra(int st, int ed, Path &solution, bool isRandom, bool isBike) const;
};

const int INF = 0x3f3f3f3f;

void Graph::loadMap(int nodeNum, const vector<MapNode> &nodeData, const vector<EdgeData> &edgeData)
{
    vertex_count = nodeNum;
    nodes = nodeData;
    edges.resize(nodeNum);
    for (const auto &i : edgeData)
        edges[i.st].push_back({i.id, i.st, i.ed, i.length, 0, i.level});
}

void Graph::loadPort(const vector<PortNode> &portData, double _scale)
{
    ports = portData;
    scale = _scale;
}

void Graph::setSpeed(int curTime)
{
    if (lastTime > curTime)lastTime -= 24 * 60 * 60;
    if (curTime - lastTime <= 15 * 60)return;
    normal_distribution<double> u{340, 50};
    default_random_engine e(time(nullptr));
    for (auto &i:nodes)
        i.speed = u(e);
    for (auto &i:edges)
        for (auto &j:i)
            j.speed = (nodes[j.st].speed + nodes[j.ed].speed) / 2;
    lastTime = curTime;
}

int Graph::dijkstra(int st, int ed, Path &solution, bool isRandom, bool isBike) const
{
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> q;
    vector<int> dis(vertex_count);
    vector<int> lastNode(vertex_count);
    for (int i = 0; i < vertex_count; ++i)
    {
        lastNode[i] = -1;
        dis[i] = INF;
    }
    dis[st] = 0;
    q.push(make_pair(0, st));
    while (!q.empty())
    {
        auto u = q.top().second;
        if (u == ed)break;
        q.pop();
        for (const auto &edge:edges[u])
        {
            if (isBike && !edge.level) continue; // 鍙兘璧拌嚜琛岃溅閬�
            if (dis[edge.ed] > dis[u] + edge.length / ((isRandom ? edge.speed : avgSpeed) / (isBike ? 1 : 3)))
            {
                dis[edge.ed] = dis[u] + edge.length / ((isRandom ? edge.speed : avgSpeed) / (isBike ? 1 : 3));
                lastNode[edge.ed] = edge.st;
                q.push(make_pair(dis[edge.ed], edge.ed));
            }
        }
    }
    int ret = dis[ed];
    solution.clear();
    solution.push_back(&nodes[ed]);
    while (~lastNode[ed])
    {
        solution.push_back(&nodes[lastNode[ed]]);
        ed = lastNode[ed];
    }
    reverse(solution.begin(), solution.end());
    return ret;
}
