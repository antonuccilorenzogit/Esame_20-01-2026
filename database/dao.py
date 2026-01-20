from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def read_nodi(n_alb):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.name
                    from artist a, album a2 
                    where a.id = a2.artist_id 
                    group by a.id, a.name 
                    having count(*) >= %s """

        cursor.execute(query, (n_alb,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        print(result)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_archi(dict_nodi):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.id as id1, a4.id as id2, count(distinct t.genre_id ) as peso
                    from artist a, album a2, track t , track t2 , album a3, artist a4
                    where a.id = a2.artist_id
                    and t.album_id = a2.id 
                    and t.genre_id = t2.genre_id 
                    and t.album_id <> t2.album_id 
                    and t2.album_id = a3.id 
                    and a3.artist_id = a4.id 
                    and a4.id <> a.id 
                    group by a.id, a4.id """

        cursor.execute(query)
        for row in cursor:
            id1=row['id1']
            id2=row['id2']
            if id1 in dict_nodi and id2 in dict_nodi:
                a1 = dict_nodi[id1]
                a2 = dict_nodi[id2]
                result.append([a1,a2,row['peso']])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def lista_artisti_ammissibili(id, d_min):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a.id
                    from artist a, album al, track t 
                    where a.id =al.artist_id and t.album_id =al.id 
                    and t.milliseconds >= 3.2*60*1000
                    group by a.id 
                    having count(*) >1 """

        cursor.execute(query)
        for row in cursor:
                result.append(row['id'])
        cursor.close()
        conn.close()
        return result