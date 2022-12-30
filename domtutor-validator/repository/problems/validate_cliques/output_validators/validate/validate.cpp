#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "validate.h"


bool compare_lines(const std::vector<int>& a, const std::vector<int>& b) {
    // compare two lines by their number of integer and by the number of each integer
    if (a.size() != b.size()) {
        return a.size() < b.size();
    }
    for (int i = 0; i < a.size(); i++) {
        if (a[i] != b[i]) {
            return a[i] < b[i];
        }
    }    
    // compare their sum
    int sum_a = 0;
    int sum_b = 0;
    for (int i = 0; i < a.size(); i++) {
        sum_a += a[i];
        sum_b += b[i];
    }
    return sum_a < sum_b;
}
std::vector<std::vector<int>> read_lines(std::istream& input) {
    std::vector<std::vector<int>> lines;
    std::string line;
    while (std::getline(input, line)) {
        std::vector<int> elements;
        std::istringstream iss(line);
        int x;
        while (iss >> x) {
            elements.push_back(x);
        }
        lines.push_back(elements);
    }
    return lines;
}

int main(int argc, char **argv) {

    init_io(argc, argv);

    // Read the lines from the input stream
    std::vector<std::vector<int>> judge_lines = read_lines(judge_ans);
    std::vector<std::vector<int>> author_lines = read_lines(author_out);

    // Sort the elements in each line
    for (std::vector<int>& line : judge_lines) {
        std::sort(line.begin(), line.end());
    }
    for (std::vector<int>& line : author_lines) {
        std::sort(line.begin(), line.end());
    }

    // Sort the lines
    std::sort(judge_lines.begin(), judge_lines.end(), compare_lines);
    std::sort(author_lines.begin(), author_lines.end(), compare_lines);

    // compare the lines
    if (judge_lines != author_lines) {
        wrong_answer("not the same clique !");
    }
    accept();
}
