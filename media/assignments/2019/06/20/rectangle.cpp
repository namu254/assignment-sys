#include <iostream>
#include<math.h>
using namespace std;

class rectangle{
	public:
	void input(){
		int dimension;
		//input length or width
		cin>>dimension;
		
	}
	int compute_area(int length, int width){
		int area;
		area = length *width;
		return area;
	}
	int compute_perimeter(int length, int width){
		int perimeter;
		perimeter = 2*(length +width);
		return perimeter;
	}
};

int main(){
	int length, width,area,perimeter;
	//initialise rectangle object
	rectangle rect;
	//call input() to enter length or width
	cout<<"Enter length of the rectangle\n";
	length = rect.input();
	cout<<"Enter width of the rectangle\n";
	width = rect.input();
	//compute area
	area =rect.compute_area(length,width);
	cout<<"Area of the rectangle is:\t"<<area<<"\n";
	perimeter = rect.compute_perimeter(length,width);
	cout<<"perimeter of the rectangle is:\t"<<perimeter<<"\n";
	return 0;
}
