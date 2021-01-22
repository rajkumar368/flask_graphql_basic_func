from graphene import Int
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User,Post
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database import app,db
...

# Schema Objects
class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post

class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User



class Query(graphene.ObjectType):
    posts = graphene.List(PostObject)
    users = graphene.Field(UserObject)

    def resolve_users(self, info):
        return  User.query.first()

    def resolve_posts(self, info):
        return  Post.query.all()



class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True) 
        username = graphene.String(required=True)

    post = graphene.List(PostObject)
    success = graphene.String()
    message = graphene.Boolean()


    def mutate(self, info, title, body, username):
        user = User.query.filter_by(username=username).first()
        post = Post(title=title, body=body)
        if user is not None:
            post.author = user
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=Post.query.filter_by(title=title),message=True,success="post created sucessfully")
        

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
    
    success = graphene.String()
    message = graphene.Boolean()

    def mutate(self,info,username):
        usr = User.query.filter_by(username=username).first()
        if usr:
            return CreatePost(message=False,success="user already sucessfully")

        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return CreatePost(message=True,success="user created sucessfully")

            

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_user = CreateUser.Field()


    
schema = graphene.Schema(query=Query, mutation=Mutation)


