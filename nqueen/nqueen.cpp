// 1005031
// CSE402 - AI Sessional
// offline 5 - N-Queens Puzzle

#include <iostream>
using namespace std;


class nQueen{
	private:
		int numofQueens;
		int queenLeft;
		int count;
		int* solution = NULL;
		int* temp = NULL;
		int* temp2 = NULL;

	public:
		nQueen(int);
		~nQueen();

		void start(int);
		void printSolution();

		// BackTarck Algortihm
		bool placeNQueens(int);
		bool checkConstraints(int);

		// Forward Checking Using MRV
		int rowMRV();
		bool placeNQueensFCMRV();
		bool forwardChecking(int,int);
};


nQueen::nQueen(int a){
	count = 0;
	numofQueens = a;
	queenLeft = a;
	solution = new int[a*a];
	temp = new int[a*a];
	temp2 = new int[a*a];
}


nQueen::~nQueen(){
	delete solution;
	delete temp;
	delete temp2;
	cout << "\nFreeing Allocated Memory.\n" << endl;
}


void nQueen::start(int n){
	bool soln;
	int i = 0;

	if (n == 1){
		cout << "Backtrack Algortihm :" << endl;
		soln = this->nQueen::placeNQueens(i);
		cout << "\tTotal Available Solution : " << count << endl;
	}
	else{
		cout << "Forward Checking Algorithm Using MRV :" << endl << endl;
		cout << "2 - Queen\t1 - Available\t0 - Not Available" << endl << endl;

		for(int i=0;i<numofQueens;i++){
			for(int j=0;j<numofQueens;j++){
				*(temp+(i*numofQueens+j)) = 1;
			}
		}

		soln = this->nQueen::placeNQueensFCMRV();
	}

	if (soln == false){
		cout << "\n\tProgramm Ended." << endl;
	}
}


void nQueen::printSolution(){
	int n = 0;
	int i,j;

	cout << "\tSolution : ";
	while(n < numofQueens){
		cout << *(solution+n) << " ";
		n++;
	}
	cout << endl << endl;

	for (i=0; i<numofQueens; i++){
		for (j=0; j<numofQueens; j++){
			if (j+1 == *(solution+i)){
				cout << "\t" << "Q";
			}
			else{
				cout << "\t" << "x";
			}
		}
		cout << endl << endl;
	}
}


bool nQueen::placeNQueens(int row){
	bool flag,succ;
	if (row >= numofQueens){
		//return true;
		count++;
		cout << "\tSolution Number : " << count << endl;
		this->nQueen::printSolution();
	}

	for (int col=1; col<=numofQueens; col++){
		*(solution+row) = col;
		flag = this->nQueen::checkConstraints(row);

		if (flag == false){
			continue;
		}

		succ = this->nQueen::placeNQueens(row+1);
		if (succ == true){
			//return true;
			continue;
		}
	}

	return false;
}


bool nQueen::checkConstraints(int n){
	int i;
	for (i=0; i<n; i++){
		if (*(solution+i) == *(solution+n) || (*(solution+n)-(n-i)) == *(solution+i) || (*(solution+n)+(n-i)) == *(solution+i)){
			return false;
		}
	}

	return true;
}


bool nQueen::placeNQueensFCMRV(){
	int row,i;
	bool flag,succ;

	if (queenLeft == 0){
		//count++;
		//cout << "\tSolution Number : " << count << endl;
		this->nQueen::printSolution();
		return true;
	}

	row = this->nQueen::rowMRV();

	for (i=0; i<numofQueens; i++){
		if (*(temp+(row*numofQueens+i)) == 0){
			continue;
		}

		*(solution+row) = i+1;
		queenLeft--;
		copy(temp,temp+numofQueens*numofQueens,temp2);
		flag = this->nQueen::forwardChecking(row,i);

		if (flag == false){
			cout << "\tConstrained Satisfiction Failed. Next Try ..." << endl;
			queenLeft++;
			copy(temp2,temp2+numofQueens*numofQueens,temp);
			continue;
		}

		succ = this->nQueen::placeNQueensFCMRV();
		if (succ==true){
			return true;
			//continue;
		}
		if (succ==false){
			cout << "\tFailed, Starting From Scratch ... " << endl;
			queenLeft = numofQueens;
			for(int i=0; i<numofQueens; i++){
				for(int j=0; j<numofQueens; j++){
					*(temp+(i*numofQueens+j)) = 1;
				}
			}
		}
	}

	return false;
}


bool nQueen::forwardChecking(int row,int col){
	int i,j,k,count;
	count = 0;
	int tempRow,tempCol;

	for (i=0; i<numofQueens; i++){
		*(temp+(row*numofQueens+i)) = 0;
		*(temp+(i*numofQueens+col)) = 0;
	}

	tempRow = row;
	tempCol = col;
	while (row<numofQueens && col<numofQueens){
		*(temp+(row*numofQueens+col)) = 0;
		row++;
		col++;
	}

	row = tempRow;
	col = tempCol;
	while (row<numofQueens && col>=0){
		*(temp+(row*numofQueens+col)) = 0;
		row++;
		col--;
	}

	row = tempRow;
	col = tempCol;
	while (row>=0 && col<numofQueens){
		*(temp+(row*numofQueens+col)) = 0;
		row--;
		col++;
	}

	row = tempRow;
	col = tempCol;
	while (row>=0 && col>=0){
		*(temp+(row*numofQueens+col)) = 0;
		row--;
		col--;
	}

	row = tempRow;
	col = tempCol;
	*(temp+(row*numofQueens+col)) = 2;

	// Print Each Forward Checking Steps
	cout <<"\tSelected Row,Column : " << row+1 << "," << col+1 << endl << endl;
	for (j=0;j<numofQueens;j++){
		for (k=0;k<numofQueens;k++){
			cout << "\t" << *(temp+j*numofQueens+k);
		}
		cout << endl << endl;
	}
	cout << endl;

	for (j=0;j<numofQueens;j++){
		for (k=0;k<numofQueens;k++){
			if (*(temp+j*numofQueens+k)==1){
				count++;
				break;
			}
		}
	}

	if (count != queenLeft){
		return false;
	}

	return true;;
}


int nQueen::rowMRV(){
	int i,j,count,row,minimum;
	row = 0;
	count = 0;
	minimum= numofQueens;

	for (i=0;i<numofQueens;i++){
		for (j=0;j<numofQueens;j++){
			if (*(temp+i*numofQueens+j)==1){
				count++;
			}
		}

		if (count == numofQueens){
			row = 0;
			break;
		}

		if (count<minimum && count>0){
			minimum = count;
			row = i;
		}

		count = 0;
	}

	return row;
}


int main(){
	int num1,num2;

	while(1){
		cout << "Option : " << endl;
		cout << "\t1 - Backtrack Algortihm" << endl;
		cout << "\t2 - Forward Checking Algortihm Using MRV" << endl;
		cout << "\t0 - Exit" << endl;
		cout << endl;
		cout << "Enter a Choice(0-2) : " ;
		cin >> num2;

		if (num2 == 1 || num2 == 2){
			cout << "Enter Queen Numbers : ";
			cin >> num1 ;
			cout << endl;

			nQueen nqueen(num1);
			nqueen.start(num2);
		}

		else if (num2 == 0){
			break;
		}

		else{
			cout << "Enter a Valid Choice." << endl;
		}
	}

	return 0;
}
