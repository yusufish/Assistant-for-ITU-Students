import os
if os.path.exists(".info"):
    line_number = 0
    with open("./.info/wrapper_list0", "r") as r:
        line_number = len(r.readlines())
    
    crn_list = [None] * line_number
    lecture_codes = [None] * line_number
    lecture_names = [None] * line_number
    lecture_times = [None] * line_number
    wrapper_list = [[], crn_list, lecture_codes, [], lecture_names, lecture_times]
    lecture_credits = []
    general_gpa = 0.00
    total_credit = 0.00
    found_grade = True
    grades = []
    term_total_credit = 0.00
    
    cnt = 0
    for i in range(6):
        if len(wrapper_list[i]) == 0: continue
        with open("./.info/wrapper_list"+str(cnt), "r") as r:
            wrapper_list[i] = r.read().splitlines()
        cnt += 1
    with open("./.info/grades.txt", "r") as r:
        grades = r.read().splitlines()
    with open("./.info/lecture_credits.txt", "r") as r:
        lecture_credits = r.read().splitlines()
    with open("./.info/others.txt", "r") as r:
        term_total_credit = float(r.readline())
        general_gpa = float(r.readline())
        total_credit = float(r.readline())
        found_grade = r.readline() == "True\n"
else :
    from backup import *

from PyQt5.QtWidgets import *
import sys
import shutil

class Stacked_menu(QWidget):

    def __init__(self):
        super(Stacked_menu, self).__init__()
        self.leftlist = QListWidget ()
        self.leftlist.insertItem(0, 'GPA Calculator' )
        self.leftlist.insertItem(1, 'Schedule' )
        self.leftlist.insertItem(2, "End of Term Grades")
        self.leftlist.insertItem(3, "Log Out")
        
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)
        
        grid_menu = QGridLayout(self)
        grid_menu.setColumnStretch(0, 31)
        grid_menu.setColumnStretch(1, 132)
        grid_menu.addWidget(self.leftlist, 0, 0, 1, 1)
        grid_menu.addWidget(self.Stack, 0, 1, 40, 1)

        self.setLayout(grid_menu)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setWindowTitle('AFITUS')
        self.show()

    def stack4UI(self):
        self.logout_grid = QGridLayout()
        logout = QPushButton("Log out")
        logout.clicked.connect(self.logging_out)
        self.logout_grid.addWidget(logout)
        self.stack4.setLayout(self.logout_grid)

    def logging_out(self):
        if os.path.exists("./.info"):
            temp_folder = "./.info"
            shutil.rmtree(temp_folder)
        sys.exit()

    
    def stack1UI(self):
        self.calculated = False        
        self.entries = []
        self.notes = ["AA","BA","BB","CB","CC","DC","DD","FF","VF"]
        self.gpa = 0.00
        self.temp = (len(wrapper_list[1]) + (len(wrapper_list[1]) % 2 == 1)) // 2
        self.combo_list = []
        
        self.grades_layout = QGridLayout()
        calculate = QPushButton("Calculate")
        calculate.clicked.connect(self.gpa_calculator)
        self.grades_layout.addWidget(calculate, self.temp, 0)
        
        for i in range(self.temp):
            for j in range(2):
                if (2*i+j == len(wrapper_list[4])): break
                lecture = QLabel(wrapper_list[4][2*i+j])
                self.grade_note = QComboBox()
                self.grade_note.addItems(self.notes)
                self.grade_note.setPlaceholderText("AA")
                self.combo_list.append(self.grade_note)
                if j == 1:
                    self.grades_layout.addWidget(lecture, i, 3, 1, 2)
                    self.grades_layout.addWidget(self.grade_note, i, 5, 1, 1)
                else:
                    self.grades_layout.addWidget(lecture, i, 0, 1, 2)
                    self.grades_layout.addWidget(self.grade_note, i, 2, 1, 1)
                
        self.stack1.setLayout(self.grades_layout)
    
    def gpa_calculator(self):
        if self.calculated:
            self.grades_layout.removeWidget(self.gpa_place)
            self.grades_layout.removeWidget(self.general_gpa_place)
            self.gpa = 0.00
        
        for i in range(self.temp):
            for j in range(2):
                if (2*i+j == len(wrapper_list[4])): break
                if self.combo_list[2*i+j].currentText() == "FF" or self.combo_list[2*i+j].currentText() == "VF":
                    self.gpa += 0
                else:
                    self.gpa += (4.00 - self.notes.index(self.combo_list[2*i+j].currentText())/2) * float(lecture_credits[2*i+j])

        self.gpa /= term_total_credit
        self.gpa_place = QLabel("Your GPA: " + str(round(self.gpa, 2)))
        self.general_gpa_place = QLabel("Your Cumulative GPA: " + str(round((self.gpa*term_total_credit + general_gpa*total_credit)/(term_total_credit+total_credit), 2)))
        self.grades_layout.addWidget(self.gpa_place, self.temp, 1, 1, 2)
        self.grades_layout.addWidget(self.general_gpa_place, self.temp, 3, 1, 2)
        self.calculated = True

    def stack2UI(self):

        self.schedule = QTableWidget()
        self.schedule.setRowCount(10)
        self.schedule.setColumnCount(6)

        self.days_table = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        self.hours_table = ["08.30-09.29", "09.30-10.29", "10.30-11.29", "11.30-12.29", "12.30-13.29", "13.30-14.29", "14.30-15.29", "15.30-16.29", "16.30-17.29"]
        self.hours = ["08", "09", "10", "11", "12", "13", "14", "15", "16"]
        

        for i in range(1,6):
            self.schedule.setItem(0, i, QTableWidgetItem(self.days_table[i-1]))
        for i in range(1,10):
            self.schedule.setItem(i, 0, QTableWidgetItem(self.hours_table[i-1]))

        cnt = 0
        for i in wrapper_list[5]:
            temp = i.split()
            j = 0
            while(j < len(temp)):
                day = self.days.index(temp[j])
                init_hour = temp[j+1][:2]
                duration = int (temp[j+1][6:8]) - int(init_hour)
                for k in range(duration):
                    self.schedule.setItem(self.hours.index(init_hour)+1+k, day+1, QTableWidgetItem(wrapper_list[2][cnt]))
                j += 3
            cnt += 1

        self.schedule_layout = QVBoxLayout()
        self.schedule_layout.addWidget(self.schedule)


        self.stack2.setLayout(self.schedule_layout)
            
    def stack3UI(self):
        if found_grade:

            self.grade_table = QTableWidget()
            self.grade_table.setRowCount(len(wrapper_list[1]) + 1)
            self.grade_table.setColumnCount(2)

            self.grade_table.setItem(0, 0, QTableWidgetItem("Course Code"))
            self.grade_table.setItem(0, 1, QTableWidgetItem("Grade"))

            cnt = 0
            for i in grades:
                if i:
                    self.grade_table.setItem(cnt+1, 0, QTableWidgetItem(wrapper_list[2][cnt]))
                    self.grade_table.setItem(cnt+1, 1, QTableWidgetItem(i))
                cnt += 1

            self.grade_table_layout = QVBoxLayout()
            self.grade_table_layout.addWidget(self.grade_table)

            self.stack3.setLayout(self.grade_table_layout)
        else:
            no_grade_layout = QGridLayout()
            grade_info = QLabel("No academic grade information is available for the respective semester on the system")
            no_grade_layout.addWidget(grade_info, 0, 0)

            self.stack3.setLayout(no_grade_layout)

            
    def display(self,i):
        self.Stack.setCurrentIndex(i)

def main():
   app = QApplication(sys.argv)
   ex = Stacked_menu()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
