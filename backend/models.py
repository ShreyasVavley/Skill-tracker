from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
    certifications = relationship("UserCertification", back_populates="user")

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    website = Column(String, nullable=True)

    certifications = relationship("Certification", back_populates="organization")

class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="certifications")
    users = relationship("UserCertification", back_populates="certification")

class UserCertification(Base):
    __tablename__ = "user_certifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    certification_id = Column(Integer, ForeignKey("certifications.id"))
    issue_date = Column(Date)
    expiry_date = Column(Date)
    credential_url = Column(String, nullable=True)

    user = relationship("User", back_populates="certifications")
    certification = relationship("Certification", back_populates="users")
