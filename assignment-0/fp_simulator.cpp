
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <queue>
#include <array>

//#include <bits/stdc++.h>

using namespace std;

int CURRENT_CYCLE = 0;

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


        void write_csv(ofstream &fp){

            fp << index << ","  << unit<< " " << opd <<" " << ops1 ;

            if (unit != "FMOV.S" && unit != "FMOV.D"){
                fp<<" " << ops2;
            }

            fp << "," << issue_cycle << "," << start_cycle << "," <<complete_cycle<< "," << writeback_cycle<<",";

            fp << result_dp;

        }

        void write_json(ofstream &fp){
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

        array<Register, 32> RegisterFile;

        void write_to(int rnum, double val){

            RegisterFile[rnum].value_dp = val;
        }

        double read_from(int rnum){

            return RegisterFile[rnum].value_dp;

        }

};




class PipelineUnit{
    public:

        string name;
        bool isEmpty;
        ProcessorInstruction *instruction;
        int processing_cycles_left;

        PipelineUnit(string unit_name){
            name = unit_name;
            isEmpty = true;
            instruction = NULL;
            processing_cycles_left = -1;
        }

        void add_instruction(ProcessorInstruction *add_instruction){
            if (isEmpty){
                instruction = add_instruction;
                isEmpty = false;
                
                if(name == "START"){

                    // Instruction Cycles required for execution
                    if((*instruction).unit == "FADD.S")   
                        processing_cycles_left = 3 - 1;
                    else if ((*instruction).unit == "FADD.D")
                        processing_cycles_left = 5 - 1;
                    else if ((*instruction).unit == "FSUB.S")
                        processing_cycles_left = 3 - 1;
                    else if ((*instruction).unit == "FSUB.D")
                        processing_cycles_left = 5 - 1;
                    else if ((*instruction).unit == "FMUL.S")
                        processing_cycles_left = 4 - 1;
                    else if ((*instruction).unit == "FMUL.D")
                        processing_cycles_left = 6 - 1;
                    else if ((*instruction).unit == "FDIV.S")
                        processing_cycles_left = 10 - 1;
                    else if ((*instruction).unit == "FDIV.D")
                        processing_cycles_left = 16 - 1;
                    else if ((*instruction).unit == "FMOV.S")
                        processing_cycles_left = 1 - 1;
                    else if ((*instruction).unit == "FMOV.D")
                        processing_cycles_left = 1 - 1;
                }

                
                if(name == "ISSUE")
                    (*instruction).issue_cycle = CURRENT_CYCLE;
                else if(name == "START")
                    (*instruction).start_cycle = CURRENT_CYCLE;
                else if (name == "COMPLETE")
                    (*instruction).complete_cycle = CURRENT_CYCLE;
                else if (name == "WRITEBACK")
                    (*instruction).writeback_cycle = CURRENT_CYCLE;


            }
        }

        void remove_instruction(){
            if(!isEmpty){
                instruction = NULL;
                isEmpty = true;
            }
        }


        void debug_print(){
            cout<<"\n[DEBUG]CURRENT_CYCLE " << CURRENT_CYCLE << flush;
            cout<<" name " << name << flush;
            cout<<" isEmpty " << isEmpty << flush;
            if (instruction == NULL)
                cout<<" instruction NULL" << flush;
            else
                cout<<" instruction " << (*instruction).unit << flush;
            
            if (name == "START")
                cout<<" processing_cycles_left " << processing_cycles_left << flush;

        }
};



int main(int argc, char * argv[]){

    cout << "\n[DEBUG]Started Program"<<flush;

    if ( argc != 3 ){
        cerr<<"Usage : ./fp_simulator <input_trace> <output_csv>";
        return 1;
    }

    ifstream infile(argv[1]);
    if(!infile.is_open()){
        cerr << "Unable to open input file";
    }


    queue<ProcessorInstruction *> instructionQueue;

    PipelineUnit IssueUnit("ISSUE");
    PipelineUnit StartUnit("START");
    PipelineUnit CompleteUnit("COMPLETE");
    PipelineUnit WritebackUnit("WRITEBACK");
    
    
    string input_line;

    int index = 0;


    cout<<"\n[DEBUG] Started Reading input trace file" <<flush;

    while(getline(infile, input_line)){
        
        //cout<<"Start";
       // cout<<"\nline : "<< input_line;

        istringstream iss(input_line);

        string arrival_cycle;
        string inst_unit;

        string opd, ops1, ops2;

        iss >> arrival_cycle;
        iss >> inst_unit;
        
        iss >> opd;
        iss >> ops1;


        //cout << endl << arrival_cycle << "," << inst_unit<<"," << opd << "," <<ops1;

        ops2 = "NULL";
        if (inst_unit != "FMOV.S" && inst_unit != "FMOV.D"){
            iss >> ops2;
            //cout<<"," << ops2;
        }

        

        //cout<<"\ntest0\n";
        instructionQueue.push( new ProcessorInstruction(index, inst_unit, opd, ops1, ops2));
        //cout<<"\ntest1\n";
        



        index += 1;

       // cout<<"\nend\n";
        
    }
    cout<<"\n[DEBUG]Queue end" <<flush;
    cout<<"\n[DEBUG] Instruction Queue size is " <<  instructionQueue.size() << flush;
            

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

    json_file << "[\n" ;

    CURRENT_CYCLE = 0;
    

    cout<<"\n[DEBUG]Started Sending Instructions to pipeline" <<flush;

    IssueUnit.debug_print(); StartUnit.debug_print(); CompleteUnit.debug_print();  WritebackUnit.debug_print();
    cout <<"\n[DEBUG] -----------------------------------------";
    cout <<"\n[DEBUG] -----------------------------------------";

    while(!instructionQueue.empty() || (!WritebackUnit.isEmpty || !CompleteUnit.isEmpty || !StartUnit.isEmpty || !IssueUnit.isEmpty)){

        // Pull from Writeback to Exit
        if(!WritebackUnit.isEmpty){
            (*WritebackUnit.instruction).write_csv(csv_file);
            csv_file << endl;
            (*WritebackUnit.instruction).write_json(json_file);
            WritebackUnit.remove_instruction();
        }

        //IssueUnit.debug_print(); StartUnit.debug_print(); CompleteUnit.debug_print();  WritebackUnit.debug_print();
        //cout <<"\n[DEBUG] -----------------------------------------";

        // Pull from Complete to Writeback
        if(!CompleteUnit.isEmpty && WritebackUnit.isEmpty){
            WritebackUnit.add_instruction(CompleteUnit.instruction);
            CompleteUnit.remove_instruction();
        }

        //IssueUnit.debug_print(); StartUnit.debug_print(); CompleteUnit.debug_print();  WritebackUnit.debug_print();
        //cout <<"\n[DEBUG] -----------------------------------------";

        //Pull from Start to Complete
        if(!StartUnit.isEmpty && CompleteUnit.isEmpty){
            if(StartUnit.processing_cycles_left <= 1){
                CompleteUnit.add_instruction(StartUnit.instruction);
                StartUnit.remove_instruction();

            }else
                StartUnit.processing_cycles_left -= 1;
        }

        //IssueUnit.debug_print(); StartUnit.debug_print(); CompleteUnit.debug_print();  WritebackUnit.debug_print();
        //cout <<"\n[DEBUG] -----------------------------------------";
        
        // Pull from Issue to Start
        if(!IssueUnit.isEmpty && StartUnit.isEmpty){
            // Check for datahazards ****

            StartUnit.add_instruction(IssueUnit.instruction);
            IssueUnit.remove_instruction();
        }

        //IssueUnit.debug_print(); StartUnit.debug_print(); CompleteUnit.debug_print();  WritebackUnit.debug_print();
        //cout <<"\n[DEBUG] -----------------------------------------";
        // Pull from Instruction Queue to Issue

        if(instructionQueue.size() >= 1 && IssueUnit.isEmpty){
            ProcessorInstruction * proc_inst = instructionQueue.front();
            IssueUnit.add_instruction(proc_inst);
            instructionQueue.pop();
            
        }

        IssueUnit.debug_print(); StartUnit.debug_print(); CompleteUnit.debug_print();  WritebackUnit.debug_print();
        cout <<"\n[DEBUG] -----------------------------------------";
        cout <<"\n[DEBUG] -----------------------------------------";
        
        CURRENT_CYCLE += 1;

        //char c;
        //cin>>c;
        //if (CURRENT_CYCLE >= 2)
        //    return 1;
    }

    json_file << "\n]";




    
    






    csv_file.close();
    json_file.close();

    return 0;

}