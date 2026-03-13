import sqlite3


class DBHandler:
    def __init__(self, db_path):
        self.db_path = db_path

    def _get_conn(self):
        """Return a fresh connection with dict-like row access."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _rows(self, rows):
        """Convert sqlite3.Row list to plain dicts (JSON-serialisable)."""
        return [dict(row) for row in rows]

    # ------------------------------------------------------------------ auth
    def validation(self, status, email, password):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            if status == "As Client":
                cur.execute("SELECT user_id FROM client WHERE email=? AND password=?", (email, password))
            elif status == "As Worker":
                cur.execute("SELECT worker_id FROM worker WHERE email=? AND password=?", (email, password))
            else:
                return False
            row = cur.fetchone()
            return dict(row) if row else False
        finally:
            conn.close()

    def isAdmin(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM client WHERE email=? AND isAdmin=1", (email,))
            return cur.fetchone() is not None
        finally:
            conn.close()

    # ------------------------------------------------------------------ clients
    def insertClient(self, name, mobile, city, email, password):
        conn = self._get_conn()
        try:
            conn.execute("INSERT INTO client(name,mobile,city,email,password) VALUES (?,?,?,?,?)",
                         (name, mobile, city, email, password))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def updateClient(self, cid, name, mobile, city, email, password):
        conn = self._get_conn()
        try:
            conn.execute("UPDATE client SET name=?,mobile=?,city=?,email=?,password=? WHERE user_id=?",
                         (name, mobile, city, email, password, cid))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def isClinetExist(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM client WHERE email=?", (email,))
            return cur.fetchone() is not None
        finally:
            conn.close()

    def getClientInfo(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM client WHERE email=?", (email,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def getClientId(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM client WHERE email=?", (email,))
            return cur.fetchone()['user_id']
        finally:
            conn.close()

    def getAllClients(self):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT user_id,name,mobile,city,email,isAdmin FROM client")
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    # ------------------------------------------------------------------ workers
    def insertWorker(self, name, mobile, title, city, email, password):
        conn = self._get_conn()
        try:
            conn.execute("INSERT INTO worker(name,mobile,title,city,email,password) VALUES (?,?,?,?,?,?)",
                         (name, mobile, title, city, email, password))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def updateWorker(self, wid, name, mobile, city, title, email, password):
        conn = self._get_conn()
        try:
            conn.execute("UPDATE worker SET name=?,mobile=?,city=?,title=?,email=?,password=? WHERE worker_id=?",
                         (name, mobile, city, title, email, password, wid))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def isWorkerExist(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT worker_id FROM worker WHERE email=?", (email,))
            return cur.fetchone() is not None
        finally:
            conn.close()

    def getWorkerInfo(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM worker WHERE email=?", (email,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def getWorkerId(self, email):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT worker_id FROM worker WHERE email=?", (email,))
            return cur.fetchone()['worker_id']
        finally:
            conn.close()

    def getAllWorkers(self):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT worker_id,name,mobile,city,email,title,rating FROM worker")
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    # ------------------------------------------------------------------ jobs
    def getjobs(self):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT w.name,w.worker_id,j.job_id,w.email,w.mobile,j.job_title,w.city,w.rating,j.rate "
                "FROM worker w JOIN job j ON w.worker_id=j.worker_id")
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def getSearchedjobs(self, searchText):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT w.name,w.worker_id,j.job_id,w.email,w.mobile,j.job_title,w.city,w.rating,j.rate "
                "FROM worker w JOIN job j ON w.worker_id=j.worker_id "
                "WHERE UPPER(j.job_title) LIKE ?",
                ("%{}%".format(searchText.upper()),))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def getJobDetails(self, id):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT w.name,w.worker_id,j.job_id,w.email,w.mobile,j.job_title,w.city,j.description,w.rating,j.rate "
                "FROM worker w JOIN job j ON w.worker_id=j.worker_id WHERE j.job_id=?", (id,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def insertNewJob(self, wid, title, rate, desc):
        conn = self._get_conn()
        try:
            conn.execute("INSERT INTO job(worker_id,job_title,rate,description) VALUES (?,?,?,?)",
                         (wid, title, rate, desc))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def deletejobP(self, job_id):
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM job WHERE job_id=?", (job_id,))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def checkMyJobs(self, wid):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT job_id,job_title,rate,description FROM job WHERE worker_id=?", (wid,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    # ------------------------------------------------------------------ requests
    def sendRequest(self, jid, wid, cid):
        conn = self._get_conn()
        try:
            conn.execute("INSERT INTO requested(job_id,worker_id,client_id) VALUES (?,?,?)",
                         (jid, wid, cid))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def getRequestedJobs(self, cid):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT w.name,r.client_id,w.worker_id,j.job_id,w.email,w.mobile,j.job_title,w.city,w.rating,j.rate "
                "FROM requested r "
                "JOIN worker w ON w.worker_id=r.worker_id "
                "JOIN job j ON j.job_id=r.job_id "
                "WHERE r.client_id=?", (cid,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def checkRequestedJobs(self, wid):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT c.name,c.user_id,c.city,r.worker_id,j.job_id,c.email,c.mobile,j.job_title "
                "FROM requested r "
                "JOIN client c ON c.user_id=r.client_id "
                "JOIN job j ON j.job_id=r.job_id "
                "WHERE r.worker_id=?", (wid,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def cancelRequest(self, worker_id, job_id, client_id):
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM requested WHERE job_id=? AND worker_id=? AND client_id=?",
                         (job_id, worker_id, client_id))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    # ------------------------------------------------------------------ accepted
    def acceptRequest(self, worker_id, job_id, client_id):
        conn = self._get_conn()
        try:
            conn.execute("INSERT INTO accepted(job_id,worker_id,client_id) VALUES (?,?,?)",
                         (job_id, worker_id, client_id))
            conn.execute("DELETE FROM requested WHERE job_id=? AND worker_id=? AND client_id=?",
                         (job_id, worker_id, client_id))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()

    def getConfirmJobs(self, cid):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT w.name,w.email,a.client_id,w.worker_id,j.job_id,w.mobile,j.job_title,w.city,w.rating,j.rate "
                "FROM accepted a "
                "JOIN worker w ON w.worker_id=a.worker_id "
                "JOIN job j ON j.job_id=a.job_id "
                "WHERE a.client_id=?", (cid,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def checkConfirmJobs(self, wid):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT c.name,c.user_id,a.worker_id,j.job_id,c.email,c.mobile,j.job_title,c.city "
                "FROM accepted a "
                "JOIN client c ON c.user_id=a.client_id "
                "JOIN job j ON j.job_id=a.job_id "
                "WHERE a.worker_id=?", (wid,))
            return self._rows(cur.fetchall())
        finally:
            conn.close()

    def jobClose(self, worker_id, job_id, client_id, ratings):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT rating FROM worker WHERE worker_id=?", (worker_id,))
            row = cur.fetchone()
            current = float(row['rating']) if row else 0
            new_rating = round((current + int(ratings)) / 2, 1)
            conn.execute("UPDATE worker SET rating=? WHERE worker_id=?", (new_rating, worker_id))
            conn.execute("DELETE FROM accepted WHERE job_id=? AND worker_id=? AND client_id=?",
                         (job_id, worker_id, client_id))
            conn.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            conn.close()