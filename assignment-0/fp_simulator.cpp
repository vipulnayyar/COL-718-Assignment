
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <queue>

//#include <bits/stdc++.h>

using namespace std;

class ProcessorInstruction{
    public:
        string unit, opd, ops1, ops2;
        //string instruction;

        int index, issue_cycle, start_cycle, complete_cycle, writeback_cycle;

        float result_sp;
        double result_dp;

        ProcessorInstruction(int inst_index, string unit_name, string inst_opd, string inst_ops1, string inst_ops2 ){

            unit = unit_name;
            index = inst_index;
            opd = inst_opd;
            ops1 = inst_ops1;
            ops2 = inst_ops2;

        }


        void write_csv(ofstream fp){

            fp << index << ","  << unit<< " " << opd <<" " << ops1 ;

            if (unit != "FMOV.S" && unit != "FMOV.D"){
                fp<<" " << ops2;
            }

            fp << "," << issue_cycle << "," << start_cycle << "," <<complete_cycle<< "," << writeback_cycle<<",";

            fp << result_dp;

        }

        void write_json(ofstream fp){
            fp <<"{"<<endl;

            fp <<"\"index\": " << index <<","<<endl;
            
            fp <<"\"instr\": \"" << unit <<" " << opd<<" "<<ops1 ;
            if (unit != "FMOV.S" && unit != "FMOV.D"){
                fp<<" " << ops2;
            }
            fp <<"\","<<endl;

            fp <<"\"issue\": " << issue_cycle<<","<<endl;

            fp <<"\"start\": " << start_cycle<<","<<endl;
            fp <<"\"complete\": " << complete_cycle<<","<<endl;
            fp <<"\"writeback\": " << writeback_cycle<<","<<endl;

            fp <<"\"unit\": \"" << unit<<"\""<<endl;

            

            fp <<"}"<<endl;
        }

};


class Register{

    public:

        float value_sp;
        double value_dp;

};


class RegisterResourceManager{
    public:

};




class PipelineUnit{
    public:

        string name;

        ProcessorInstruction * instruction;

        PipelineUnit(string unit_name){
            name = unit_name;
        }
};



int main(int argc, char * argv[]){

    if ( argc != 3 ){
        cerr<<"Usage : ./fp_simulator <input_trace> <output_csv>";
        return 1;
    }

    ifstream infile(argv[1]);
    if(!infile.is_open()){
        cerr << "Unable to open input file";
    }


    queue<ProcessorInstruction> instructionQueue;


    string input_line;

    int index = 0;


    while(getline(infile, input_line)){
        
        istringstream iss(input_line);

        string arrival_cycle;
        string inst_unit;

        string opd, ops1, ops2;

        iss >> arrival_cycle;
        iss >> inst_unit;
        
        iss >> opd;
        iss >> ops1;


        cout << endl << arrival_cycle << "," << inst_unit<<"," << opd << "," <<ops1;

        if (inst_unit != "FMOV.S" && inst_unit != "FMOV.D"){
            iss >> ops2;
            cout<<"," << ops2;
        }

        ops2 = "NULL";

        instructionQueue.push(ProcessorInstruction(index, inst_unit, opd, ops1, ops2));




        index += 1;

    }

    infile.close();

    ofstream csv_file(argv[2]);
    if (!csv_file.is_open()){
        cerr << "Error in opening CSV output file";
        return 1;

    }

    ofstream json_file(string(argv[2]) + "_timeline.json");
    if (!json_file.is_open()){
        cerr << "Error in opening JSON output file";
        return 1;
        
    }



    






    csv_file.close();
    json_file.close();

    return 0;

}