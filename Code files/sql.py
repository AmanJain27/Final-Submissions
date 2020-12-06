import sqlite3
import io
import os.path
import glob
import pandas as pd

def create_haberman():
    conn = sqlite3.connect("..\\confidential_databases\\example.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS haberman")

    c.execute('''CREATE TABLE IF NOT EXISTS haberman
                 (Age, Year of Operation, No of positive auxiliary nodes, survival status)''')

    import csv
    row_t = []
    with open('..\\haberman.csv', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            row = [int(row[i]) for i in range(len(row))]
            row_t.append(tuple(row))


    #c.executemany("INSERT INTO haberman2 VALUES (?,?,?,?)",  row_t)
    # Insert a row of data

    #c.execute("SELECT COUNT(Survival) FROM haberman2 WHERE Age = 50")
    c.execute("SELECT COUNT(*) FROM haberman")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO haberman VALUES (?,?,?,?)", row_t)

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


create_haberman()


def create_anon_haberman():
    import csv
    conn = sqlite3.connect("..\\confidential_databases\\example2.db")
    c = conn.cursor()
    path = "..\\diff privacy\\"

    dirs = [name for name in os.listdir(path)]
    #print(dirs)
    k = 0
    for i in range(len(dirs)):
        for j in os.listdir(path  + dirs[i]):
            k += 1
            c.execute(f"DROP TABLE IF EXISTS haberman{k}")
            c.execute(
                f'CREATE TABLE IF NOT EXISTS haberman{k} (Age, Year of Operation, No of positive auxiliary nodes, survival status)')

            row_t = []

            # r_hb = []
            # with open('C:\\Users\\AmanH\\Downloads\\haberman.csv', newline='') as f1:
            #     reader = csv.reader(f1)
            #
            #     for r in reader:
            #         r = [int(r[i]) for i in range(len(r[:-1]))]
            #         r_hb.append(r)
            #
            #
            # with open(path + dirs[i] + "\\"+ j, newline='') as f:
            #
            #         reader = csv.reader(f)
            #
            #
            #         next(reader, None)  # skip the headers
            #         for row in reader:
            #             m = 0
            #             r_hb[m].append(row[-1])
            #             print(r_hb[m])
            #
            #             row_t.append(tuple(r_hb[m]))



            hb = pd.read_csv("..\\haberman.csv", header=None)

            hb_s = hb.iloc[:, :-1]

            hb_r = pd.read_csv(path + dirs[i] + "\\"+ j, skiprows=0)

            hb_r_q = hb_r.iloc[:, -1]

            pd_out = hb_s.assign(survival = list(hb_r_q))

            pd_out.to_csv(f"..\\sql_execution_files\\haberman{k}.csv", index=False)
            with open(f"..\\sql_execution_files\\haberman{k}.csv") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    row = [int(row[i]) for i in range(len(row))]
                    row_t.append(tuple(row))




            c.execute(f"SELECT COUNT(*) FROM haberman{k}")
            if c.fetchone()[0] == 0:
                c.executemany(f"INSERT INTO haberman{k} VALUES (?,?,?,?)", row_t)

    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    return k





def output_true_results(query, condition):
    query = "SELECT " + query + " FROM haberman WHERE " + condition

    conn = sqlite3.connect("..\\confidential_databases\\example.db")
    c = conn.cursor()
    try:
        c.execute(query)

        return c.fetchall()
    except Exception:
        return "Query Error"


def output_randomized_results(query, condition):

    true_res = output_true_results(query, condition)
    print(true_res)
    k = create_anon_haberman()


    randomized_res = []


    conn = sqlite3.connect("..\\confidential_databases\\example2.db")
    c = conn.cursor()
    for i in range(k):
        query_real = "SELECT " + query + f" FROM haberman{i+1} WHERE " + condition + ";"
        try:
            c.execute(query_real)
            randomized_res.append(c.fetchall()[0][0])
        except Exception:
            return "Query Error"
    print(randomized_res)
    unsigned_noise_induced = [abs(randomized_res[i] - true_res[0][0]) for i in range(len(randomized_res))]
    minimum_noise = min(unsigned_noise_induced)
    best_noisy_result_idx = unsigned_noise_induced.index(minimum_noise)
    best_noisy_res = randomized_res[best_noisy_result_idx]
        #print(randomized_res[best_noisy_result_idx])
    return str(best_noisy_res)









#output_randomized_results("COUNT(Survival)", "Survival = 1")
