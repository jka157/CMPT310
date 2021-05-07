//
//  main.cpp
//  finalproject
//
//  Created by John Kim on 2020-07-21.
//  Copyright © 2020 JohnKim. All rights reserved.
//

//  John (Junseong) Kim
//  301262540
//  jka157@sfu.ca
//
//  References:
//
//  TA - Mohammad's Tutorials
//  https://pyformat.info/
//  https://pynative.com/python-input-function-get-user-input/
//  https://www.programiz.com/python-programming/methods
//  https://www.mastersofgames.com/rules/reversi-othello-rules.htm
//https://www.programiz.com/cpp-programming/library-function/cstdlib/srand#:~:text=rand()%20function.-,The%20srand()%20function%20in%20C%2B%2B%20seeds%20the%20pseudo%20random,seeded%20with%20srand(1).

#include <iostream>
#include <random>
#include <cstdlib>
#include <string>
#include <array>
#include <list>
#include <vector>
#include <cmath>
#include <algorithm>
#include <stack>
#include <queue>
#include <deque>
#include <ctime>
#include <iterator>
#include <utility>
#include <tuple>
#include <chrono>

using namespace std;
using namespace std::chrono;


// Function to print board
void display(vector <string> board) {

        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[0]<<" | "<<board[1]<<" | "<<board[2]<<" | "<<board[3]<<" | "<<board[4]<<" | "<<board[5]<<" | "<<board[6]<<" | "<<board[7]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[8]<<" | "<<board[9]<<" | "<<board[10]<<" | "<<board[11]<<" | "<<board[12]<<" | "<<board[13]<<" | "<<board[14]<<" | "<<board[15]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[16]<<" | "<<board[17]<<" | "<<board[18]<<" | "<<board[19]<<" | "<<board[20]<<" | "<<board[21]<<" | "<<board[22]<<" | "<<board[23]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[24]<<" | "<<board[25]<<" | "<<board[26]<<" | "<<board[27]<<" | "<<board[28]<<" | "<<board[29]<<" | "<<board[30]<<" | "<<board[31]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[32]<<" | "<<board[33]<<" | "<<board[34]<<" | "<<board[35]<<" | "<<board[36]<<" | "<<board[37]<<" | "<<board[38]<<" | "<<board[39]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[40]<<" | "<<board[41]<<" | "<<board[42]<<" | "<<board[43]<<" | "<<board[44]<<" | "<<board[45]<<" | "<<board[46]<<" | "<<board[47]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[48]<<" | "<<board[49]<<" | "<<board[50]<<" | "<<board[51]<<" | "<<board[52]<<" | "<<board[53]<<" | "<<board[54]<<" | "<<board[55]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
        cout << "| "<<board[56]<<" | "<<board[57]<<" | "<<board[58]<<" | "<<board[59]<<" | "<<board[60]<<" | "<<board[61]<<" | "<<board[62]<<" | "<<board[63]<<" | " << endl;
        cout << "*---*---*---*---*---*---*---*---*" << endl;
    
        cout<<" "<<endl;
        
    
};

// Function that checks the possible moves that can be made
auto checkMoves(vector <string> board_position, int move, int turn){
    int index;
    int size_array;
    int temp_b;
    string variable_string;
    vector <int> black_positions;
    vector <int> white_positions;
    vector <int> positions;
    vector <int> available_moves;
    vector<vector <int>> flips;
    bool valid = false;
    

    for (int i = 0; i < 64; i++){
        
        if (board_position[i] == "B"){
            black_positions.push_back(i);
        }
        
        if (board_position[i] == "W"){
            white_positions.push_back(i);
        }
    }
        
    if (turn == 1 || turn == 3){
        size_array = black_positions.size();
        string variable_string("B");
    
    }
    
    else {
        size_array = white_positions.size();
        string variable_string("W");
        
    }
    
    for (int j = 0; j < size_array; j++){
        
        if (turn == 1 || turn == 3){
            temp_b = black_positions[j];
            positions = white_positions;
        }
        else{
            temp_b = white_positions[j];
            positions = black_positions;
        }
        
    
        cout << "\nChecking available moves for: "<< temp_b << endl;
      
        
        //Sees if the value exists in the array:
        bool exists_right = find(begin(positions), end(positions), temp_b+1) != end(positions);
        bool exists_left = find(begin(positions), end(positions), temp_b-1) != end(positions);
        bool exists_up = find(begin(positions), end(positions), temp_b-8) != end(positions);
        bool exists_down = find(begin(positions), end(positions), temp_b+8) != end(positions);
        bool exists_UL = find(begin(positions), end(positions), temp_b-9) != end(positions);
        bool exists_UR = find(begin(positions), end(positions), temp_b-7) != end(positions);
        bool exists_DL = find(begin(positions), end(positions), temp_b+7) != end(positions);
        bool exists_DR = find(begin(positions), end(positions), temp_b+9) != end(positions);
        
        // Traverse Right
        if (exists_right == true){
            bool more_right = true;
            index = 1;
            vector<int> flips_right;
            flips_right.push_back(temp_b);
            
            while (more_right == true){
               
                
                bool more_right = find(begin(positions), end(positions), temp_b + index) != end(positions);
                
                if (more_right == false && (board_position[temp_b + index] == " " || board_position[temp_b + index] == variable_string)){
                    
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b + index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b + index);
                    }
                    cout << temp_b + index << endl;
                    valid = true;
                    
                    if (turn == 1 & move == temp_b + index){
                        flips_right.push_back(move);
                        flips.push_back(flips_right);
                    }
                    
                    else if (turn == 2 || turn == 3){
                        flips_right.push_back(temp_b + index);
                        flips.push_back(flips_right);
                    }

                    break;
                }
                
                flips_right.push_back(temp_b + index);
                index++;
                if (temp_b + index > 63 || temp_b + index < 0 || temp_b + index == 8 || temp_b + index == 16 || temp_b + index == 24 || temp_b + index == 32 || temp_b + index == 40 || temp_b + index == 48 || temp_b + index == 56){
                    break;
                    
                }
                
            }
            
            
        }
        
        // Traverse Left
        if (exists_left == true){
            bool more_left = true;
            index = 1;
            vector<int> flips_left;
            flips_left.push_back(temp_b);
            
            while (more_left == true){
                
                bool more_left = find(begin(positions), end(positions), temp_b - index) != end(positions);
                
                if  (more_left == false && (board_position[temp_b - index] == " " || board_position[temp_b - index] == variable_string)){
                   
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b - index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b - index);
                    }
                    cout << temp_b - index << endl;
                    valid = true;
                    
                    if (turn == 1 && move == temp_b - index){
                        flips_left.push_back(move);
                        flips.push_back(flips_left);
                    }
                    else if (turn == 2 || turn == 3){
                        flips_left.push_back(temp_b - index);
                        flips.push_back(flips_left);
                    }
                    
                    break;
                }
                flips_left.push_back(temp_b - index);
                index++;
                if (temp_b - index > 63 || temp_b - index < 0 || temp_b - index == 7 || temp_b - index == 15 || temp_b - index == 23 || temp_b - index == 31 || temp_b - index == 39 || temp_b - index == 47 || temp_b - index == 55){
                    break;
                    
                }
            }
            
        }
        
        // Traverse Up
        if (exists_up == true){
            bool more_up = true;
            index = 8;
            vector<int> flips_up;
            flips_up.push_back(temp_b);
            
            while (more_up == true){
                
                bool more_up = find(begin(positions), end(positions), temp_b - index) != end(positions);
                
                if  (more_up == false && (board_position[temp_b - index] == " " || board_position[temp_b - index] == variable_string)){
                
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b - index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b - index);
                    }
                    cout << temp_b - index << endl;
                    valid = true;
                    
                    if (turn == 1 && move == temp_b - index){
                        flips_up.push_back(move);
                        flips.push_back(flips_up);
                    }
                    else if (turn == 2 || turn == 3) {
                        flips_up.push_back(temp_b - index);
                        flips.push_back(flips_up);
                    }
                   
                    break;
                }
                flips_up.push_back(temp_b - index);
                index = 8 + index;
                if (temp_b - index > 63 || temp_b - index < 0){
                    break;
                    
                }
              
            }
            
        }
        
        // Traverse Down
        if (exists_down == true){
            bool more_down = true;
            index = 8;
            vector<int> flips_down;
            flips_down.push_back(temp_b);
            
            while (more_down == true){
                
                bool more_down = find(begin(positions), end(positions), temp_b + index) != end(positions);
                
                if (more_down == false && (board_position[temp_b + index] == " " || board_position[temp_b + index] == variable_string)){
                    
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b + index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b + index);
                    }
                    cout << temp_b + index << endl;
                    valid = true;
                    
                    if (turn == 1 && move == temp_b + index){
                        flips_down.push_back(move);
                        flips.push_back(flips_down);
                    }
                    else if (turn == 2 || turn == 3){
                        flips_down.push_back(temp_b + index);
                        flips.push_back(flips_down);
                    }
                    
                    break;
                }
                
                flips_down.push_back(temp_b + index);
                index = 8 + index;
                if (temp_b + index > 63 || temp_b + index < 0){
                    break;
                    
                }
              
            }
            
        }
        
        // Traverse Diagonal - Up & Left
        if (exists_UL == true){
            bool more_UL = true;
            index = 9;
            vector<int> flips_UL;
            flips_UL.push_back(temp_b);
           
            
            while (more_UL == true){
                
                bool more_UL = find(begin(positions), end(positions), temp_b - index) != end(positions);
                
                if (more_UL == false && (board_position[temp_b - index] == " " || board_position[temp_b - index] == variable_string)){
                    
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b - index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b - index);
                    }
                    cout << temp_b - index << endl;
                    valid = true;
                    
                    if (turn == 1 && move == temp_b - index){
                        flips_UL.push_back(move);
                        flips.push_back(flips_UL);
                        
                    }
                    else if (turn == 2 || turn == 3){
                        flips_UL.push_back(temp_b - index);
                        flips.push_back(flips_UL);
                    }
                    
                    break;
                }
                
                flips_UL.push_back(temp_b - index);
                index = 9 + index;
                if (temp_b - index > 63 || temp_b - index < 0 || temp_b - index == 55 || temp_b - index == 47 || temp_b - index == 39 || temp_b - index == 31 || temp_b - index == 23 || temp_b - index == 15 || temp_b - index == 7){
                    break;
                    
                }
              
            }
            
        }
        
        // Traverse Diagonal - Up & Right
        if (exists_UR == true){
            bool more_UR = true;
            index = 7;
            vector<int> flips_UR;
            flips_UR.push_back(temp_b);
            
            while (more_UR == true){
                
                bool more_UR = find(begin(positions), end(positions), temp_b - index) != end(positions);
                
                if (more_UR == false && (board_position[temp_b - index] == " " || board_position[temp_b - index] == variable_string)){
                    
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b - index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b - index);
                    }
                    cout << temp_b - index << endl;
                    valid = true;
                    
                    if (turn == 1 && move == temp_b - index){
                        flips_UR.push_back(move);
                        flips.push_back(flips_UR);
                    }
                    else if (turn == 2 || turn == 3){
                        flips_UR.push_back(temp_b - index);
                        flips.push_back(flips_UR);
                    }
                   
                    break;
                }
                
                flips_UR.push_back(temp_b - index);
                index = 7 + index;
                if (temp_b - index > 63 || temp_b - index <= 0 || temp_b - index == 56 || temp_b - index == 48 || temp_b - index == 40 || temp_b - index == 32 || temp_b - index == 24 || temp_b - index == 16 || temp_b - index == 8){
                    break;
                    
                }
              
            }
            
        }
        
        // Traverse Diagonal - Down & Left
        if (exists_DL == true){
            bool more_DL = true;
            index = 7;
            vector<int> flips_DL;
            flips_DL.push_back(temp_b);
            
            while (more_DL == true){
                
                bool more_DL = find(begin(positions), end(positions), temp_b + index) != end(positions);
                
                if (more_DL == false && (board_position[temp_b + index] == " " || board_position[temp_b + index] == variable_string)){
                    
                    bool duplicate = find(begin(available_moves), end(available_moves), temp_b + index) != end(available_moves);
                    if (duplicate == false){
                        available_moves.push_back(temp_b + index);
                    }
                    cout << temp_b + index << endl;
                    valid = true;
                    
                    if (turn == 1 && move == temp_b + index){
                        flips_DL.push_back(move);
                        flips.push_back(flips_DL);
                    }
                    else if (turn == 2 || turn == 3){
                        flips_DL.push_back(temp_b + index);
                        flips.push_back(flips_DL);
                        
                    }
                    flips_DL.push_back(temp_b + index);
                    break;
                }
                
                flips_DL.push_back(temp_b + index);
                index = 7 + index;
                if (temp_b + index > 63 || temp_b + index < 0 || temp_b + index == 7 || temp_b + index == 15 || temp_b + index == 23 || temp_b + index == 31 || temp_b + index == 39 || temp_b + index == 47 || temp_b + index == 55 || temp_b + index == 63){
                    break;
                    
                }
              
            }
            
        }
        
        // Traverse Diagonal - Down & Right
               if (exists_DR == true){
                   bool more_DR = true;
                   index = 9;
                   vector<int> flips_DR;
                   flips_DR.push_back(temp_b);
                   
                   while (more_DR == true){
                       
                       bool more_DR = find(begin(positions), end(positions), temp_b + index) != end(positions);
                       
                       if (more_DR == false && (board_position[temp_b + index] == " " || board_position[temp_b + index] == variable_string)){
                           
                           bool duplicate = find(begin(available_moves), end(available_moves), temp_b + index) != end(available_moves);
                           if (duplicate == false){
                               available_moves.push_back(temp_b + index);
                           }
                           cout << temp_b + index << endl;
                           valid = true;
                           
                           if (turn == 1 && move == temp_b + index){
                               flips_DR.push_back(move);
                               flips.push_back(flips_DR);
                           }
                           else if (turn == 2 || turn == 3){
                               flips_DR.push_back(temp_b + index);
                               flips.push_back(flips_DR);
                           }

                           break;
                       }
                       
                       flips_DR.push_back(temp_b + index);
                       index = 9 + index;
                       if (temp_b + index > 63 || temp_b + index < 0 || temp_b + index == 16 || temp_b + index == 24 || temp_b + index == 32 || temp_b + index == 40 || temp_b + index == 48 || temp_b + index == 56){
                           break;
                           
                       }
                     
                   }
                   
               }
     
    }
    
    int array_size = available_moves.size();
    
//    for (int i = 0; i < flips.size(); i++){
//        for (int j = 0; j < flips[i].size(); j++){
//            //cout << "This is the flips: " << flips[i][j] << endl;
//
//        }
//    }
 
    auto tp = make_tuple(available_moves, valid, array_size, flips);
    return tp;
    
};


//Function to get user input - double checks if the input is incorrect
auto getInput(vector <string> board_position){

    int input = 0;
    int player_move = 1;
    vector<int> to_flip;
    vector<vector <int>> flip_target;
    int number_moves;
    bool accepted_move = false;
    bool valid_move;
    vector <int> possible_moves;
    vector <string> copy = board_position;
    
    
    while (accepted_move == false) {
        cout << "Pick the position you want to place your black stone (0-63)" << endl;
        cin >> input;
        cout <<" "<< endl;
        
        
        // Input not in range?
        if (input < 0 || input > 63){
            cout << "Pick a position in the right range (0-63) \n" << endl;
        }
        
        else {
            
        //Check if the input is a valid move
            auto answers = checkMoves(board_position, input, player_move);
            possible_moves = get<0>(answers);
            valid_move = get<1>(answers);
            number_moves = get<2>(answers);
            flip_target = get<3>(answers);
            
            if (possible_moves.empty() == true){
                cout << "No available move" << endl;
                int size = to_flip.size();
                auto top = make_tuple(input, to_flip, size);
                return top;
                   
            }
            
            else{
                
                if (valid_move == true){
                    
                    for (int i = 0; i < number_moves; i ++){
                        int temp = possible_moves[i];
                        copy[temp] = "O";

                   }
                    cout << " " << endl;
                    
                    bool exists = find(begin(possible_moves), end(possible_moves), input) != end(possible_moves);
                    if (exists == true){
                        
                        cout << flip_target.size() << endl;
                        
                        for (int i = 0; i < possible_moves.size(); i++){
                            cout << possible_moves[i] << endl;
                        }
                        
                        
                        accepted_move = true;
                    }
                    
                    // Displays the board with possible moves circled on the board
                    else{
                        cout <<"Not a valid move, pick from one of the possible moves with the circle" << endl;
                        display(copy);
                    }
                    
               }
                
             }
            
        }
        
        
    }
    
    // Get the stones that need to be flipped corresponding to the input
    
    for (int i = 0; i < flip_target.size(); i++){
        for (int j = 0; j < flip_target[i].size(); j++){
            to_flip.push_back(flip_target[i][j]);
        }
    }
    
    int size = to_flip.size();
    auto top = make_tuple(input, to_flip, size);
    return top;
    
};

// Modified Monte Carlo Heuristics
auto modified_Carlo(vector <string> board_vector, bool simulate, int position, bool pick){
    
    int my_turn = 3;
    bool valid_mod_move = false;
    vector<int> mod_comp_move;
    vector<int> go_flip;
    vector<vector <int>> turns;
    vector<int> moves_to_simulate;
    int picked_move;
    int flipping_size;
    int random_element;
    int LTC = 0;
    int RTC = 7;
    int LBC = 56;
    int RBC = 63;
    
     
    cout << "Modified Computer's turn: " << endl;
     
    auto monte_tuple = checkMoves(board_vector, NULL, my_turn);
    mod_comp_move = get<0>(monte_tuple);
    valid_mod_move = get<1>(monte_tuple);
    flipping_size = get<2>(monte_tuple);
    turns = get<3>(monte_tuple);
     
    if (simulate == true){
        
        bool corner_move1 = find(begin(mod_comp_move), end(mod_comp_move), LTC) != end(mod_comp_move);
        bool corner_move2 = find(begin(mod_comp_move), end(mod_comp_move), RTC) != end(mod_comp_move);
        bool corner_move3 = find(begin(mod_comp_move), end(mod_comp_move), LBC) != end(mod_comp_move);
        bool corner_move4 = find(begin(mod_comp_move), end(mod_comp_move), RBC) != end(mod_comp_move);
        
        // Checks for corner moves - if there is a corner move, it will be chosen
        if (mod_comp_move.empty() == true){
            auto mod_tuple = make_tuple(picked_move, flipping_size, go_flip, mod_comp_move);
            return mod_tuple;
        }
        
        else if (corner_move1 == true){
            cout <<"Corner move is favored" << endl;
            picked_move = LTC;
        }
        
        else if (corner_move2 == true){
            cout <<"Corner move is favored" << endl;
            picked_move = RTC;
        }
        
        else if (corner_move3 == true){
            cout <<"Corner move is favored" << endl;
            picked_move = LBC;
        }
        
        else if (corner_move4 == true){
            cout <<"Corner move is favored" << endl;
            picked_move = RBC;
        }
        
        else{
            random_element = rand() % mod_comp_move.size();
            picked_move = mod_comp_move[random_element];
            cout << "This is the computer's chosen move " << picked_move << endl;
        }
       
    }
    
    else{
        if (pick == true){
            picked_move = position;
            cout << turns.size();
            
        }
        else{
            
            if (mod_comp_move.empty() == true){
                picked_move = 0;
            }
            else{
                picked_move = mod_comp_move[position];
            }

        }
        
    }
     
    for (int i = 0; i < turns.size(); i++){
          bool move_exists = find(begin(turns[i]), end(turns[i]), picked_move) != end(turns[i]);
          
          for (int j = 0; j < turns[i].size(); j++){
              
              if (move_exists == true){
                  go_flip.push_back(turns[i][j]);
              }
              
          }
    }
    
    
    flipping_size = go_flip.size();
    auto mod_tuple = make_tuple(picked_move, flipping_size, go_flip, mod_comp_move);

    return mod_tuple;
    
};

// This does the random playouts
auto monte_Carlo(vector <string> board_Array){
    
    int who_turn = 2;
    bool valid_comp_move = false;
    vector<int> comp_move;
    vector<int> need_flip;
    vector<vector <int>> to_turn;
    vector <int> temp_array;
    int chosen_move;
    int flip_size;
    int rand_element;
    
    
    cout << "Computer's Turn: " << endl;
    
    while (valid_comp_move == false){
        
        auto monte_tuple = checkMoves(board_Array, NULL, who_turn);
        comp_move = get<0>(monte_tuple);
        valid_comp_move = get<1>(monte_tuple);
        flip_size = get<2>(monte_tuple);
        to_turn = get<3>(monte_tuple);
                
        if (comp_move.empty() == true){
            cout << "No available moves for the computer" << endl;
            auto Carlo_tuple = make_tuple(chosen_move, flip_size, need_flip);
            return Carlo_tuple;
            
        }
        else{
            rand_element = rand() % comp_move.size();
            chosen_move = comp_move[rand_element];
            cout << "\nThis is the computer's chosen move \n" << chosen_move << endl;
        }
        
        
    }
    
     for (int i = 0; i < to_turn.size(); i++){
         bool move_exists = find(begin(to_turn[i]), end(to_turn[i]), chosen_move) != end(to_turn[i]);
         
         for (int j = 0; j < to_turn[i].size(); j++){
             
             if (move_exists == true){
                 need_flip.push_back(to_turn[i][j]);
             }
             
         }
     }
    
     flip_size = need_flip.size();

    auto Carlo_tuple = make_tuple(chosen_move, flip_size, need_flip);
    
    return Carlo_tuple;
};

// Checks if the game is done and outputs the result
auto checkGame (vector <string> checkGame, int status){
    
    int num_player = 0;
    int num_computer = 0;
    int result = 0;
    
    
    for (int i = 0; i < 64; i++){
        if (checkGame[i] == "B"){
            num_player++;
        }
        else if (checkGame[i] == "W"){
            num_computer ++;
        }
        
    }
    
    if (status == 1){
        if (num_player > num_computer){
            cout << "Player wins the game" << endl;
            cout << "Player: " << num_player << "   Computer: " << num_computer << endl;
        }
        
        else if (num_player < num_computer){
            cout << "Computer wins the game" << endl;
            cout << "Player: " << num_player << "   Computer: " << num_computer << endl;
        }
        
        else {
            cout << "The game was a draw" << endl;
            cout << "Player: " << num_player << "   Computer: " << num_computer << endl;
        }
    }
    
    else{
        if (num_player > num_computer){
           cout << "Modified computer wins the game" << endl;
           cout << "Modified Computer: " << num_player << "   Computer: " << num_computer << endl;
            result = 1;
       }
       
       else if (num_player < num_computer){
           cout << "Computer wins the game" << endl;
           cout << "Modified Computer: " << num_player << "   Computer: " << num_computer << endl;
           result = 2;
       }
       
       else {
           cout << "The game was a draw" << endl;
           cout << "Modified Computer: " << num_player << "   Computer: " << num_computer << endl;
           result = 3;
       }
    
    }
    
    auto game_tuple = make_tuple(true, result);
    return game_tuple;
    
};

// Simulation function
auto recursive_simulation(vector<string> the_board){
    auto time_spent = 0;
    int count = 1;
    int index = 0;
    int mod_comp = 0;
    int comp_win = 0;
    int draw = 0;
    bool simulation = false;
    bool done = false;
    
    vector <int> flip_sim;
    vector <int> simulation_array;
    vector <int> computer_sim;
    vector <string> temp_array;
    
    int hello;
    

    
    
    temp_array = the_board;
    // Before the simulation, get the possible positions
    auto modified_tuple = modified_Carlo(the_board, simulation, index, false);
    int sim_move = get<0>(modified_tuple);
    int length_sim = get<1>(modified_tuple);
    flip_sim = get<2>(modified_tuple);
    simulation_array = get<3>(modified_tuple);
    
    int size_simulation = simulation_array.size();
    vector <int> game_points(size_simulation);

    
    if (sim_move == 0 || sim_move == 7 || sim_move == 56 || sim_move == 63){
        auto results = make_tuple(mod_comp, comp_win, draw, game_points, simulation_array);
        return results;
    }

        
    for (int i = 0; i < size_simulation; i++){
                    
        the_board = temp_array;
        // display(the_board);
        simulation = false;
        
        if (index >= 1){
            auto modified_tuple = modified_Carlo(the_board, simulation, index, false);
            int sim_move = get<0>(modified_tuple);
            int length_sim = get<1>(modified_tuple);
            flip_sim = get<2>(modified_tuple);
            
            if (sim_move == 0 || sim_move == 7 || sim_move == 56 || sim_move == 63){
                  auto results = make_tuple(mod_comp, comp_win, draw, game_points, simulation_array);
                  return results;
              }

        }
        else{
            sim_move = simulation_array[i];
            the_board[sim_move] = "B";
        }
        
        for (int j = 0; j < length_sim; j++){
            the_board[flip_sim[j]] = "B";
      
        }
        
        display(the_board);
        //cout << "IS THIS WORKING" << endl;
        //cin >> hello;
        simulation = true;
        
    
        while (time_spent < 2 && done == false){
            
            bool cannot_comp = true;
            bool cannot_sim = true;

             auto start = high_resolution_clock::now();

             auto comp_tuple = monte_Carlo(the_board);
             int computer_move = get<0>(comp_tuple);
             int length_comp = get<1>(comp_tuple);
             computer_sim = get<2>(comp_tuple);

             the_board[computer_move] = "W";


             for (int j = 0; j < length_comp; j++){
                 the_board[computer_sim[j]] = "W";
                 // cout << "Computer turning:" << computer_sim[j] << endl;
             }
            
            display(the_board);
            
            if (computer_sim.empty() == true){
                cannot_comp = false;
            }
            
            bool done_yet = find(begin(the_board), end(the_board), " ") != end(the_board);
            if (done_yet == false){
                auto game = checkGame(the_board, 2);
                bool done = get<0>(game);
                int result_game = get<1>(game);
                
                if (result_game == 1){
                    mod_comp ++;
                    game_points[i] = 10;
                }
                else if (result_game == 2){
                    comp_win ++;
                    game_points[i] = -10;
                }
                else {
                    draw ++;
                    game_points[i] = 3;
                }
                
                break;
            }

            auto modified_tuple = modified_Carlo(the_board, simulation, index, false);
           int sim_move = get<0>(modified_tuple);
           int length_sim = get<1>(modified_tuple);
           flip_sim = get<2>(modified_tuple);
           
            if (flip_sim.empty() == true){
                cannot_sim = false;
                
            }
           

           the_board[sim_move] = "B";
           for (int j = 0; j < length_sim; j++){
               the_board[flip_sim[j]] = "B";
               // cout << "Modified turning:" << flip_sim[j] << endl;
           }
            
            display(the_board);

            count ++;
            
            
            if (cannot_sim == false && cannot_comp == false){
                cout << "Cannot continue the game" << endl;
                auto game = checkGame(the_board, 2);
                bool done = get<0>(game);
                break;
            }

            auto stop = high_resolution_clock::now();
            auto duration = duration_cast<seconds>(stop-start);
            time_spent = time_spent + duration.count();
            // cout <<"This is the time it took to complete the simulation (s): "<< time_spent << endl;
            
        }
        
        
        index ++;
    }
    
    auto results = make_tuple(mod_comp, comp_win, draw, game_points, simulation_array);
    return results;
    
};



int main(){
    auto time_spent = 0;
    bool gameStatus = false;
    
    
    string go;
    vector <string> check_board;
    vector <int> simulated_moves;
    vector <int> scores;
    vector <int> stones_flip_player;
    vector <int> stones_flip_computer;
    vector <int> stones_flip_mod;
    vector <int> flip;
    int state_board[64] = {};
    int choice;
    int index = 1;
    int lose = 0;
    int win = 0;
    int draw = 0;
    
    cout <<"Player will be playing as black - B, Computer will be playing as white - W" << endl;
    cout <<"Get ready to play! \n" << endl;
    
    cout <<"Select the computer's algorithm (1 or 2): 1 - Monte Carlo Tree Search, 2- Modified Heuristics" << endl;
    cin >> choice;
    
    // Initalize board
    for (int i = 0; i < 64; ++i){
        if (i == 27 || i == 36){
            //check_board[i] = "B";
            check_board.push_back("B");
            state_board[i] = i;
        }
        else if (i == 28 || i == 35){
            // check_board[i] = "W";
            check_board.push_back("W");
            state_board[i] = i;
        }
        else
            // check_board[i] = " ";
            check_board.push_back(" ");
            state_board[i] = i;
    }
    
    srand((unsigned) time(0));
    
    while (gameStatus == false) {
        
        bool comp_nomore = true;
        bool mod_nomore = true;
        
        if (choice == 1){
            
            if (index == 1){
                cout << "You've chosen 1 - Monte Carlo Tree Search \n" << endl;
                display(check_board);
            }
            
            // Get user input for the position of the stone and place it there:
            auto your_move_tuple = getInput(check_board);
            int your_move = get<0>(your_move_tuple);
            stones_flip_player = get<1>(your_move_tuple);
            int length_player = get<2>(your_move_tuple);
            
            if (stones_flip_player.empty() == true){
                cout << "Skipping turn" << endl;
            }
            
            else{
                check_board[your_move] = "B";
                
                            
                for (int i = 0; i < length_player; i++){
                    check_board[stones_flip_player[i]] = "B";
                    // cout << "Player turning: " << stones_flip_player[i] << endl;
                }
            
            
            }
            
            index ++;
            display(check_board);
            
            
            auto comp_tuple = monte_Carlo(check_board);
            int computer_move = get<0>(comp_tuple);
            int length_comp = get<1>(comp_tuple);
            stones_flip_computer = get<2>(comp_tuple);
            
            if (stones_flip_computer.empty() == true){
                cout <<"Skipping turn" << endl;
            }
            else{
                
                check_board[computer_move] = "W";
           
                for (int j = 0; j < length_comp; j++){
                    check_board[stones_flip_computer[j]] = "W";
                }
                
            }
            
            
            index ++;
            
            display(check_board);

            
        }
                
        else if (choice == 2){
            
            if (index == 1){
                cout << "You've chosen 2 - Modified Heuristics" << endl;
                display(check_board);
            }
            
            auto start = high_resolution_clock::now();
            for (int i = 0; i < 10; i ++){
                auto simulated_results = recursive_simulation(check_board);
                int winner_modd = get<0>(simulated_results);
                int winner_computer = get<1>(simulated_results);
                int was_draw = get<2>(simulated_results);
                vector<int> winner = get<3>(simulated_results);
                simulated_moves = get<4>(simulated_results);
                
                win = winner_modd + win;
                lose = winner_computer + lose;
                draw = was_draw + draw;
                
                for (int j = 0; j < winner.size(); j ++){
                    if (i == 0){
                        scores.push_back(winner[j]);
                    }
                    else{
                        scores[j] = scores[j] + winner[j];
                    }
                    
                }
            }
            
            auto stop = high_resolution_clock::now();
            auto duration = duration_cast<seconds>(stop-start);
            time_spent = time_spent + duration.count();
            cout <<"This is the time it took in seconds to complete the simulation: "<< time_spent << endl;
            
            cout << "Scores" << endl;
            for (int x = 0; x < scores.size(); x ++){
                cout << scores[x] << endl;
            }
            
            int max_index = max_element(scores.begin(), scores.end()) - scores.begin();
            cout << max_index << endl;
            cout << simulated_moves[max_index] << endl;
            int chosen_move = simulated_moves[max_index];
            
            auto simulate_tuple = modified_Carlo(check_board, false, chosen_move, true);
            vector<int> need_flips = get<2>(simulate_tuple);

            
            if (need_flips.empty() == true){
                cout << "Skipping turn" << endl;
                mod_nomore = false;
            }
            
            
            check_board[simulated_moves[max_index]] = "B";
            for (int k = 0; k < need_flips.size(); k++){
                check_board[need_flips[k]] = "B";
                cout << need_flips[k] << endl;
            }

            
            cout << "This was the result: Modified Heuristics - " << win << " Computer - " << lose << " Draw - " << draw << endl;
            
            display(check_board);
            
            cout << "This is the move chosen by the simulation: " << endl;
            cout << "Press Enter to continue" << endl;
            
            if (index == 1){
                cin.ignore();
            }
            cin.ignore();
            
             
             auto comp_tuple = monte_Carlo(check_board);
             int computer_move = get<0>(comp_tuple);
             int length_comp = get<1>(comp_tuple);
             stones_flip_computer = get<2>(comp_tuple);
            
            if (stones_flip_computer.empty() == true){
                cout << "Skipping turn" << endl;
                comp_nomore = false;
            }
            
            else{
                check_board[computer_move] = "W";
                
                for (int j = 0; j < length_comp; j++){
                    check_board[stones_flip_computer[j]] = "W";
                    // cout << "Computer turning:" << stones_flip_computer[j] << endl;
                }
               
            }
             
             index ++;
             display(check_board);
            cout << "This is the board after the computer has made it's move " << endl;
            cout << "Press Enter to continue" << endl;
            cin.ignore();
            
            
            
            if (mod_nomore == false && comp_nomore == false){
                auto checked_game = checkGame(check_board, choice);
                gameStatus = get<0>(checked_game);
                break;
            }
             
        
            
        }
        
        else {
            cout << "Enter valid choice, 1 or 2" << endl;
            cin >> choice;
            
        }
        
 
        bool not_done = find(begin(check_board), end(check_board), " ") != end(check_board);
        if (not_done == false){
            auto checked_game = checkGame(check_board, choice);
            gameStatus = get<0>(checked_game);
        }
    }
    
    
    
    
    return 0;
    
}

