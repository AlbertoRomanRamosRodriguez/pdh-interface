#include <iostream>
#include <array>
#include <string>
#include <fstream>
#include <ctime>
using namespace std;

int main() {
    clock_t start, end;
    start = clock();
   
    string filenames[10][10] = {
	{
		"/output/10_left.jpeg",
		"/output/1444_left.jpeg",
		"/output/16_right_ly4JThy.jpeg",
		"/output/79_left.jpeg",
		"/output/1177_right.jpeg",
		"/output/1509_right.jpeg",
		"/output/30_left.jpeg",
		"/output/129_right.jpeg",
		"/output/16_right.jpeg",
		"/output/367_right.jpeg"
	},
	{
		"10_left.jpeg",
		"1444_left.jpeg",
		"16_right_ly4JThy.jpeg",
		"79_left.jpeg",
		"1177_right.jpeg",
		"1509_right.jpeg",
		"30_left.jpeg",
		"129_right.jpeg",
		"16_right.jpeg",
		"367_right.jpeg"
	}	
	};
    
    for (int i = 0; i < 10; i++){
		std::ifstream  src(filenames[0][i], std::ios::binary);
		std::ofstream  dst(filenames[1][i], std::ios::binary);
		dst << src.rdbuf();
	}


    end = clock();

    cout << "CPU-TIME START " << start << "\n";
    cout << "CPU-TIME END " << end << "\n";
    cout << "CPU-TIME END - START " << end - start << "\n";
    cout << "TIME(SEC) " << static_cast<double>(end - start) / CLOCKS_PER_SEC << "\n";

    return 0;
}
