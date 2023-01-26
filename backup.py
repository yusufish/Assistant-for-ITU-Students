import os
path = "./"
if os.path.exists(".info"):
    pass

else:
    from data_scraping import wrapper_list, lecture_credits, term_total_credit, general_gpa, total_credit, found_grade, grades, remember_me
    if remember_me:
        os.mkdir("./.info")
        cnt = 0
        for each_list in wrapper_list:
            if len(each_list) == 0: continue
            with open("./.info/wrapper_list"+str(cnt), "w") as f:
                for element in each_list:
                    f.write(element+"\n")
            cnt += 1
        with open("./.info/lecture_credits.txt", "w") as f:
            for credit in lecture_credits:
                f.write(credit+"\n")
        with open("./.info/others.txt", "w") as f:
            f.write(str(term_total_credit)+"\n")
            f.write(str(general_gpa)+"\n")
            f.write(str(total_credit)+"\n")
            f.write(str(found_grade)+"\n")
        with open("./.info/grades.txt", "w") as f:
            if found_grade:
                for grade in grades:
                    f.write(grade+"\n")
