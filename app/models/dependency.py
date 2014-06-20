from app import db
from base import Base
from association_objects import DependencyInSentence
from sqlalchemy.ext.associationproxy import association_proxy

class Dependency(db.Model, Base):
    """A representation of the grammatical dependency between two words.

    Each dependency is comprised of a governor, a dependent, and a grammatical
    relationship.

    Attributes:
      grammatical_relationship_id (int): link to the grammatical relationship
      governor_id (int): link to the governor word
      dependent_id (int): link to the dependent word
      sentence_count (int): the number of sentences this appears in
      document_count (int): the number of documents this appears in

    Relationships:
      has one: dependent (Word), governor (Word), grammatical relationship
      has many: sentences
    """

    # Attributes

    grammatical_relationship_id = db.Column(
        db.Integer, db.ForeignKey("grammatical_relationship.id")
    )
    governor_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    dependent_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    sentence_count = db.Column(db.Integer, index=True)
    document_count = db.Column(db.Integer, index=True)

    # Relationships

    grammatical_relationship = db.relationship(
        "GrammaticalRelationship", backref="dependency"
    )
    governor = db.relationship(
        "Word", foreign_keys=[governor_id], backref="governor_dependencies"
    )
    dependent = db.relationship(
        "Word", foreign_keys=[dependent_id], backref="dependent_dependencies"
    )

    sentences = association_proxy("dependency_in_sentence", "sentence",
        creator=lambda sentence: DependencyInSentence(sentence=sentence)
    )

    def __repr__(self):
        """Representation string for the dependency
        """

        rel = self.grammatical_relationship.name
        gov = self.governor.word
        dep = self.dependent.word

        return "<Dependency: " + rel + "(" + gov + ", " + dep + ") >"

