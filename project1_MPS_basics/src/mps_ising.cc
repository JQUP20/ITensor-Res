// MPS基础: 横场伊辛模型 (ITensor C++实现)
// 编译: g++ -std=c++17 mps_ising.cc -o mps_ising -litensor
// 运行: ./mps_ising

#include "itensor/all.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

using namespace itensor;
using namespace std;

// 计算纠缠熵
double entanglement_entropy(const MPS& psi, int b) {
    // 在键b处计算纠缠熵
    psi.position(b);

    auto l = leftLinkIndex(psi, b);
    auto s = siteIndex(psi, b);

    auto wf = psi(b);
    auto U = psi(b);
    ITensor S, V;
    auto spectrum = svd(wf, U, S, V);

    double SvN = 0.0;
    for(auto p : spectrum.eigs()) {
        if(p > 1e-14) {
            SvN -= p * log(p);
        }
    }

    return SvN;
}

// 主程序
int main(int argc, char* argv[]) {
    // 参数
    int N = 40;           // 系统大小
    double J = 1.0;       // 耦合强度
    double h = 0.5;       // 横场
    int maxm = 64;        // 最大键维度
    double cutoff = 1e-12; // 截断误差

    // 解析命令行参数
    if(argc > 1) N = atoi(argv[1]);
    if(argc > 2) h = atof(argv[2]);
    if(argc > 3) maxm = atoi(argv[3]);

    cout << "========================================" << endl;
    cout << "横场伊辛模型 (ITensor C++)" << endl;
    cout << "========================================" << endl;
    cout << "系统大小: N = " << N << endl;
    cout << "横场: h = " << h << endl;
    cout << "最大键维度: maxm = " << maxm << endl;
    cout << "========================================" << endl;

    // 构建格点
    auto sites = SpinHalf(N);

    // 构建哈密顿量 (MPO)
    auto ampo = AutoMPO(sites);
    for(int j = 1; j < N; ++j) {
        ampo += -J, "Sz", j, "Sz", j+1;
    }
    for(int j = 1; j <= N; ++j) {
        ampo += -h, "Sx", j;
    }
    auto H = toMPO(ampo);

    // 初始态（随机）
    auto state = InitState(sites);
    for(int i = 1; i <= N; ++i) {
        state.set(i, i%2 == 1 ? "Up" : "Dn");
    }
    auto psi = MPS(state);

    // DMRG参数
    auto sweeps = Sweeps(10);
    sweeps.maxdim() = 10, 20, maxm/2, maxm;
    sweeps.cutoff() = cutoff;
    sweeps.niter() = 2;
    sweeps.noise() = 1e-7, 1e-8, 0.0;

    cout << "\n运行DMRG..." << endl;
    cout << sweeps << endl;

    // 运行DMRG
    auto [energy, psi_gs] = dmrg(H, psi, sweeps, {"Quiet=", false});

    cout << "\n结果:" << endl;
    cout << "基态能量: E = " << energy << endl;
    cout << "每格点能量: E/N = " << energy/N << endl;

    // 计算纠缠熵
    cout << "\n计算纠缠熵分布..." << endl;
    vector<double> entropies;
    for(int b = 1; b < N; ++b) {
        double S = entanglement_entropy(psi_gs, b);
        entropies.push_back(S);

        if(b % 10 == 0 || b == N/2) {
            cout << "键 " << b << ": S = " << S << endl;
        }
    }

    // 保存数据
    string filename = "entanglement_cpp_h" + to_string(h) + ".dat";
    ofstream datafile(filename);
    datafile << "# Position Entropy\n";
    for(size_t i = 0; i < entropies.size(); ++i) {
        datafile << i+1 << " " << entropies[i] << "\n";
    }
    datafile.close();

    cout << "\n数据已保存到: " << filename << endl;

    // 计算磁化
    cout << "\n磁化强度分布:" << endl;
    for(int j = 1; j <= min(5, N); ++j) {
        psi_gs.position(j);
        auto sz = elt(dag(prime(psi_gs(j), "Site"))
                     * sites.op("Sz", j)
                     * psi_gs(j));
        cout << "格点 " << j << ": <Sz> = " << sz << endl;
    }

    cout << "\n========================================" << endl;
    cout << "计算完成！" << endl;
    cout << "========================================" << endl;

    return 0;
}
