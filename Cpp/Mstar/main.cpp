//
// Created by Jeroen on 22/05/2020.
//
#include "Mstar.h"
using namespace std;

int main() {
    // Problem 17
    vector<vector<int>> grid{{0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0},
                             {1, 1, 1, 0, 1, 1, 1},
                             {1, 1, 1, 0, 1, 1, 1},
                             {1, 1, 1, 0, 1, 1, 1},
                             {0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0}};
    vector<pair<int, int>> v_I_a{std::make_pair(1, 0), std::make_pair(6, 1), std::make_pair(0, 6),
                                 std::make_pair(5, 6)};
    std::vector<std::vector<std::pair<int, int>>> v_W_a{{std::make_pair(-1, -1)},
                                                        {std::make_pair(-1, -1)},
                                                        {std::make_pair(-1, -1)},
                                                        {std::make_pair(-1, -1)}};
    vector<pair<int, int>> v_F_a{std::make_pair(1, 5), std::make_pair(3, 6), std::make_pair(5, 0),
                                 std::make_pair(3, 0)};
//    // Problem 15 aka TSP
//    vector<vector<int>> grid{{0, 0, 0, 0, 0, 0, 0},
//                             {0, 1, 1, 0, 0, 0, 1},
//                             {0, 1, 1, 1, 1, 0, 1},
//                             {0, 0, 1, 1, 0, 0, 1},
//                             {1, 1, 1, 1, 0, 0, 1},
//                             {0, 0, 0, 0, 0, 0, 0}};
//    vector<pair<int, int>> v_I_a{std::make_pair(6, 0), std::make_pair(0, 5)};
//    std::vector<std::vector<std::pair<int, int>>> v_W_a{{std::make_pair(5,4), std::make_pair(0,3), std::make_pair(1,5)},
//                                                        {std::make_pair(1,3), std::make_pair(4,1), std::make_pair(4,3)}};
//    vector<pair<int, int>> v_F_a{std::make_pair(6, 5), std::make_pair(5, 5)};
    Mstar lol = Mstar(grid, v_I_a, v_W_a, v_F_a, true);
    std::vector<std::vector<std::pair<int, int>>> res = lol.solve().first;
    for (const auto& agent : res) {
        cout << "[";
        for (const auto& loc : agent) {
            cout << "(" << loc.first << ", " << loc.second << "), ";
        }
        cout << "]" << endl;
    }
    return 0;
}
