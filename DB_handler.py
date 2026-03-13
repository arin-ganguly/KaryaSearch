import pymysql
from pymysql.cursors import DictCursor


class DBHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def _get_conn(self):
        """Open and return a fresh (db, cursor) pair. Always use in a try/finally."""
        db = pymysql.connect(
            host=self.host, user=self.user,
            password=self.password, database=self.database
        )
        cursor = db.cursor(DictCursor)
        return db, cursor

    # ------------------------------------------------------------------ auth
    def validation(self, status, email, password):
        db, cursor = self._get_conn()
        try:
            if status == "As Client":
                cursor.execute("SELECT user_id FROM client WHERE email=%s AND password=%s", (email, password))
            elif status == "As Worker":
                cursor.execute("SELECT worker_id FROM worker WHERE email=%s AND password=%s", (email, password))
            else:
                return False
            return cursor.fetchone() or False
        finally:
            cursor.close(); db.close()

    def isAdmin(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT user_id FROM client WHERE email=%s AND isAdmin=1", (email,))
            return cursor.fetchone() is not None
        finally:
            cursor.close(); db.close()

    # ------------------------------------------------------------------ clients
    def insertClient(self, name, mobile, city, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO `client`(`name`,`mobile`,`city`,`email`,`password`) VALUES (%s,%s,%s,%s,%s)",
                (name, mobile, city, email, password))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def updateClient(self, cid, name, mobile, city, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "UPDATE `client` SET `name`=%s,`mobile`=%s,`city`=%s,`email`=%s,`password`=%s WHERE user_id=%s",
                (name, mobile, city, email, password, cid))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def isClinetExist(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT user_id FROM client WHERE email=%s", (email,))
            return cursor.fetchone() is not None
        finally:
            cursor.close(); db.close()

    def getClientInfo(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT * FROM client WHERE email=%s", (email,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def getClientId(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT user_id FROM client WHERE email=%s", (email,))
            return cursor.fetchone()['user_id']
        finally:
            cursor.close(); db.close()

    def getAllClients(self):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT user_id,name,mobile,city,email,isAdmin FROM client")
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    # ------------------------------------------------------------------ workers
    def insertWorker(self, name, mobile, title, city, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO `worker`(`name`,`mobile`,`title`,`city`,`email`,`password`) VALUES (%s,%s,%s,%s,%s,%s)",
                (name, mobile, title, city, email, password))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def updateWorker(self, wid, name, mobile, city, title, email, password):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "UPDATE `worker` SET `name`=%s,`mobile`=%s,`city`=%s,`title`=%s,`email`=%s,`password`=%s WHERE worker_id=%s",
                (name, mobile, city, title, email, password, wid))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def isWorkerExist(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT worker_id FROM worker WHERE email=%s", (email,))
            return cursor.fetchone() is not None
        finally:
            cursor.close(); db.close()

    def getWorkerInfo(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT * FROM worker WHERE email=%s", (email,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def getWorkerId(self, email):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT worker_id FROM worker WHERE email=%s", (email,))
            return cursor.fetchone()['worker_id']
        finally:
            cursor.close(); db.close()

    def getAllWorkers(self):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT worker_id,name,mobile,city,email,title,rating FROM worker")
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    # ------------------------------------------------------------------ jobs
    def getjobs(self):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT name,w.worker_id,job_id,email,mobile,job_title,city,rating,rate "
                "FROM worker w, job j WHERE w.worker_id=j.worker_id")
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def getSearchedjobs(self, searchText):
        db, cursor = self._get_conn()
        try:
            search = "%{}%".format(searchText.upper())
            cursor.execute(
                "SELECT name,w.worker_id,job_id,email,mobile,job_title,city,rating,rate "
                "FROM worker w, job j WHERE w.worker_id=j.worker_id AND UPPER(j.job_title) LIKE %s",
                (search,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def getJobDetails(self, id):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT name,w.worker_id,job_id,email,mobile,job_title,city,description,rating,rate "
                "FROM worker w, job j WHERE w.worker_id=j.worker_id AND job_id=%s", (id,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def insertNewJob(self, wid, title, rate, desc):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO `job`(`worker_id`,`job_title`,`rate`,`description`) VALUES (%s,%s,%s,%s)",
                (wid, title, rate, desc))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def deletejobP(self, job_id):
        db, cursor = self._get_conn()
        try:
            cursor.execute("DELETE FROM job WHERE job_id=%s", (job_id,))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def checkMyJobs(self, wid):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT job_id,job_title,rate,description FROM job WHERE worker_id=%s", (wid,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    # ------------------------------------------------------------------ requests
    def sendRequest(self, jid, wid, cid):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO `requested`(`job_id`,`worker_id`,`client_id`) VALUES (%s,%s,%s)",
                (jid, wid, cid))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def getRequestedJobs(self, cid):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT w.name,r.client_id,w.worker_id,j.job_id,w.email,w.mobile,job_title,w.city,rating,rate "
                "FROM worker w, job j, requested r "
                "WHERE w.worker_id=r.worker_id AND j.job_id=r.job_id AND r.client_id=%s", (cid,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def checkRequestedJobs(self, wid):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT c.name,c.user_id,c.city,r.worker_id,j.job_id,c.email,c.mobile,job_title "
                "FROM client c, job j, requested r "
                "WHERE c.user_id=r.client_id AND j.job_id=r.job_id AND r.worker_id=%s", (wid,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def cancelRequest(self, worker_id, job_id, client_id):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "DELETE FROM requested WHERE job_id=%s AND worker_id=%s AND client_id=%s",
                (job_id, worker_id, client_id))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    # ------------------------------------------------------------------ accepted
    def acceptRequest(self, worker_id, job_id, client_id):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "INSERT INTO `accepted`(`job_id`,`worker_id`,`client_id`) VALUES (%s,%s,%s)",
                (job_id, worker_id, client_id))
            db.commit()
            cursor.execute(
                "DELETE FROM requested WHERE job_id=%s AND worker_id=%s AND client_id=%s",
                (job_id, worker_id, client_id))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()

    def getConfirmJobs(self, cid):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT w.name,w.email,r.client_id,w.worker_id,j.job_id,w.mobile,job_title,w.city,rating,rate "
                "FROM worker w, job j, accepted r "
                "WHERE w.worker_id=r.worker_id AND j.job_id=r.job_id AND r.client_id=%s", (cid,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def checkConfirmJobs(self, wid):
        db, cursor = self._get_conn()
        try:
            cursor.execute(
                "SELECT c.name,c.user_id,r.worker_id,j.job_id,c.email,c.mobile,job_title,c.city "
                "FROM client c, job j, accepted r "
                "WHERE c.user_id=r.client_id AND j.job_id=r.job_id AND r.worker_id=%s", (wid,))
            return cursor.fetchall()
        finally:
            cursor.close(); db.close()

    def jobClose(self, worker_id, job_id, client_id, ratings):
        db, cursor = self._get_conn()
        try:
            cursor.execute("SELECT rating FROM worker WHERE worker_id=%s", (worker_id,))
            row = cursor.fetchone()
            current = float(row['rating']) if row else 0
            new_rating = round((current + int(ratings)) / 2, 1)
            cursor.execute("UPDATE `worker` SET `rating`=%s WHERE worker_id=%s", (new_rating, worker_id))
            db.commit()
            cursor.execute(
                "DELETE FROM accepted WHERE job_id=%s AND worker_id=%s AND client_id=%s",
                (job_id, worker_id, client_id))
            db.commit()
            return True
        except Exception as e:
            print(e); return False
        finally:
            cursor.close(); db.close()