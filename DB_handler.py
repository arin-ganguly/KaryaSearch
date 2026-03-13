import sqlite3


class DBHandler:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_conn(self):
        db = sqlite3.connect(self.db_path)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        return db, cursor

    # ------------------------------------------------------------------ auth
    def validation(self, status, email, password):
        db, cursor = self._get_conn()
        try:
            if status == "As Client":
                cursor.execute(
                    "SELECT user_id FROM client WHERE email=? AND password=?",
                    (email, password),
                )
            elif status == "As Worker":
                cursor.execute(
                    "SELECT worker_id FROM worker WHERE email=? AND password=?",
                    (email, password),
                )
            else:
                return False
            row = cursor.fetchone()
            return dict(row) if row else False
        finally:
            cursor.close()
            db.close()

    def isAdmin(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT user_id FROM client WHERE email=? AND isAdmin=1", (email,)
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            db.close()

    # ------------------------------------------------------------------ clients
    def insertClient(self, name, mobile, city, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO client(name,mobile,city,email,password) VALUES (?,?,?,?,?)",
                (name, mobile, city, email, password),
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def updateClient(self, cid, name, mobile, city, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "UPDATE client SET name=?,mobile=?,city=?,email=?,password=? WHERE user_id=?",
                (name, mobile, city, email, password, cid),
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def isClinetExist(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT user_id FROM client WHERE email=?", (email,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            db.close()

    def getClientInfo(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT * FROM client WHERE email=?", (email,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    def getClientId(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT user_id FROM client WHERE email=?", (email,))
            row = cursor.fetchone()
            return row["user_id"] if row else None
        finally:
            cursor.close()
            db.close()

    def getAllClients(self):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT user_id,name,mobile,city,email,isAdmin FROM client"
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    # ------------------------------------------------------------------ workers
    def insertWorker(self, name, mobile, title, city, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO worker(name,mobile,title,city,email,password) VALUES (?,?,?,?,?,?)",
                (name, mobile, title, city, email, password),
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def updateWorker(self, wid, name, mobile, city, title, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "UPDATE worker SET name=?,mobile=?,city=?,title=?,email=?,password=? WHERE worker_id=?",
                (name, mobile, city, title, email, password, wid),
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def isWorkerExist(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT worker_id FROM worker WHERE email=?", (email,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            db.close()

    def getWorkerInfo(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT * FROM worker WHERE email=?", (email,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    def getWorkerId(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT worker_id FROM worker WHERE email=?", (email,))
            row = cursor.fetchone()
            return row["worker_id"] if row else None
        finally:
            cursor.close()
            db.close()

    def getAllWorkers(self):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT worker_id,name,mobile,city,email,title,rating FROM worker"
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    # ------------------------------------------------------------------ jobs
    def getjobs(self):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT name,w.worker_id,job_id,email,mobile,job_title,city,rating,rate "
                "FROM worker w JOIN job j ON w.worker_id=j.worker_id"
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    def getSearchedjobs(self, searchText):
        db, cursor = self._get_conn()
        try:
            search = "%" + searchText.upper() + "%"
            cursor.execute(
                "SELECT name,w.worker_id,job_id,email,mobile,job_title,city,rating,rate "
                "FROM worker w JOIN job j ON w.worker_id=j.worker_id "
                "WHERE UPPER(j.job_title) LIKE ?",
                (search,),
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    def getJobDetails(self, id):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT name,w.worker_id,job_id,email,mobile,job_title,city,description,rating,rate "
                "FROM worker w JOIN job j ON w.worker_id=j.worker_id WHERE job_id=?",
                (id,),
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()

    def insertNewJob(self, wid, title, rate, desc):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO job(worker_id,job_title,rate,description) VALUES (?,?,?,?)",
                (wid, title, rate, desc),
            )
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def deletejobP(self, job_id):
        db, cursor = self._get_conn()
        try:
            cursor.execute("DELETE FROM job WHERE job_id=?", (job_id,))
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def checkMyJobs(self, wid):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT job_id,job_title,rate,description FROM job WHERE worker_id=?",
                (wid,),
            )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            cursor.close()
            db.close()