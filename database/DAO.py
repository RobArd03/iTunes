from database.DB_connect import DBConnect
from model.Album import Album


class DAO():

    @staticmethod
    def getAlbums(dMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT a.*, sum(t.Milliseconds)/60000 as dTot
                    from album a , track t 
                    where a.AlbumId = t.AlbumId 
                    GROUP BY a.AlbumId
                    HAVING dTot > %s
                """

        cursor.execute(query, (dMin,)) # dMin in minuti

        result=[]
        for row in cursor:
            result.append(Album(**row))

        return result


    @staticmethod
    def getAllEdges(idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT DISTINCT t1.AlbumId as a1 , t2.AlbumId as a2
                    FROM track t1, track t2 , playlisttrack p1, playlisttrack p2  
                    WHERE t1.AlbumId < t2.AlbumId
                    AND p1.PlaylistId = p2.PlaylistId 
                    AND t1.TrackId = p1.TrackId
                    AND t2.TrackId = p2.TrackId
                """

        cursor.execute(query)

        result=[]
        for row in cursor:
            n1 = idMap.get(row["a1"])
            n2 = idMap.get(row["a2"])
            if n1 is not None and n2 is not None:
                result.append( ( n1 , n2 ) )

        return result



