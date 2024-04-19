from neo4j import GraphDatabase


class NDB:
    def __init__(self, url, username, password):
        self.driver = GraphDatabase.driver(url, auth=(username, password))

    def __execute_write(self, tx, subject, relation, _object):
        query = (
            "MERGE (e1:Entity {name: $subject}) "
            "MERGE (e2:Entity {name: $object}) "
            "MERGE (e1)-[r:RELATIONSHIP {type: $relation}]->(e2)"
        )
        tx.run(query, subject=subject, relation=relation, object=_object)

    def add_triplet(self, subject: str, relation: str, _object: str):
        with self.driver.session() as session:
            session.execute_write(self.__execute_write, subject, relation, _object)

    def __find_triplets(self, tx, subject: str):
        query = (
            "MATCH (e1:Entity {name: $subject})-[r:RELATIONSHIP]->(e2:Entity) "
            "RETURN e1.name, r.type, e2.name"
        )
        result = tx.run(query, subject=subject)
        return [(record["e1.name"], record["r.type"], record["e2.name"]) for record in result]

    def find_triplets(self, subject: str):
        with self.driver.session() as session:
            return session.execute_read(self.__find_triplets, subject)
    def __clear_graph(self, tx):
        query = (
            "MATCH (n) DETACH DELETE n"
        )
        tx.run(query)
    
    def clear_all(self):
        with self.driver.session() as session:
            session.execute_write(self.__clear_graph)

    def close(self):
        self.driver.close()

    def __del__(self):
        self.close()
