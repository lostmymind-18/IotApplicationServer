from urllib import response
from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'IotServer'

mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM info ORDER BY time DESC LIMIT 1''')
    result = cursor.fetchall()[0]
    temp = result[1]
    humid = result[2]
    mysql.connection.commit()
    cursor.close()
    data = [time()*1000,temp,humid]
    response = make_response(json.dumps(data,indent=4,sort_keys=True, default=str))
    response.content_type = 'application/json'
    return response


if __name__ == "__main__":
    app.run(debug=True)


Program([VarDecl("x"),FuncDecl("foo",[VarDecl("x")],[],[Assign(Id("x"),FloatLit(2))])],[Assign(Id("x"),IntLit(3)),CallStmt("foo",[Id("x")])])

class StaticCheck(Visitor):
    def visitProgram(self,ctx,o):
        o = [{}]
        for decl in ctx.decl:
            self.visit(decl,o)
        for stmt in ctx.stmts:
            self.visit(stmt,o)
    
    def visitVarDecl(self,ctx,o):
        if ctx.name in o[0]:
            raise Redeclared(ctx)
        o[0][ctx.name] = 0
    
    def visitFuncDecl(self,ctx,o):
        a = {}
        for param in ctx.param:
            self.visit(param,[a])
            o[0][ctx.name]=a
        env = [({},a)] + o
        for decl in ctx.local:
            self.visit(decl,env)
        for stmt in ctx.stmts:
            self.visit(stmt,env)
        b = []
        for param in ctx.param:
            b+=a[param.name]
        o[0][ctx.name] = b
            
    def visitCallStmt(self,ctx,o):
        for ox in o:
            if ctx.name in ox and type(ox[ctx.name]) == list:
                paras = ox[ctx.name]
                args = ctx.args
                if len(paras) != len(ctx.args):
                    raise TypeMismatchInStatement(ctx)
                for i in range (0,len(paras)):
                    args[i] = self.visit(args[i],o)
                    if paras[i] == 0 and args[i] == 0:
                        raise TypeCannotBeInferred(ctx)
                    if paras[i] == 0:
                        paras[i] = args[i]
                    else if paras[i] != args[i]:
                        raise TypeMismatchInStatement(ctx)
            else:
                raise UndeclaredIdentifier(ctx.name)
                
                
    
    def visitAssign(self,ctx:Assign,o):
        rhs = self.visit(ctx.rhs,o)
        lhs = self.visit(ctx.lhs,o)
        if lhs == 0 and rhs == 0:
            raise TypeCannotBeInferred(ctx)
        if lhs == 0:
            for ox in o:
                if type(ox) == tuple:
                    if ctx.lhs.name in ox[0] and type(ox[0][ctx.lhs.name]) != dict:
                        ox[0][ctx.lhs.name] = rhs
                        break
                    if ctx.lhs.name in ox[1] and type(ox[1][ctx.lhs.name]) != dict:
                        ox[1][ctx.lhs.name] = rhs
                        break
                else:
                    if ctx.lhs.name in ox and type(ox[ctx.lhs.name]) != dict:
                        ox[ctx.lhs.name] = rhs
                        break
            lhs = rhs
        if rhs == 0:
            for ox in o:
                if type(ox) == tuple:
                    if ctx.rhs.name in ox[0] and type(ox[0][ctx.rhs.name]) != dict:
                        ox[0][ctx.rhs.name] = lhs
                        break
                    if ctx.rhs.name in ox[1] and type(ox[1][ctx.rhs.name]) != dict:
                        ox[1][ctx.rhs.name] = lhs
                        break
                else:
                    if ctx.rhs.name in ox and type(ox[ctx.rhs.name]) != dict:
                        ox[ctx.rhs.name] = lhs
                        break
            rhs = lhs
        if lhs != rhs:
            raise TypeMismatchInStatement(ctx)
        
    def visitBinOp(self,ctx:BinOp,o): 
        op=ctx.op
        t1=self.visit(ctx.e1,o)
        t2=self.visit(ctx.e2,o)
        if op in ['+','-','*','/']:
            if t1 == 0:
                o[0][ctx.e1.name] = 1
                t1 = 1
            if t2 == 0:
                o[0][ctx.e2.name] = 1
                t2 = 1
            if t1 != 1 or t2 != 1:
                raise TypeMismatchInExpression(ctx)
            return 1
        if op in ['+.','-.','*.','/.']:
            if t1 == 0:
                o[0][ctx.e1.name] = 2
                t1 = 2
            if t2 == 0:
                o[0][ctx.e2.name] = 2
                t2 = 2
            if t1 != 2 or t2 != 2:
                raise TypeMismatchInExpression(ctx)
            return 2
        if op in ['>','=']:
            if t1 == 0:
                o[0][ctx.e1.name] = 1
                t1 = 1
            if t2 == 0:
                o[0][ctx.e2.name] = 1
                t2 = 1
            if t1 != 1 or t2 != 1:
                raise TypeMismatchInExpression(ctx)
            return 3
            
        if op in ['>.','=.']:
            if t1 == 0:
                o[0][ctx.e1.name] = 2
                t1 = 2
            if t2 == 0:
                o[0][ctx.e2.name] = 2
                t2 = 2
            if t1 != 2 or t2 != 2:
                raise TypeMismatchInExpression(ctx)
            return 3
        
        if op in ['&&','||','>b','=b']:
            if t1 == 0:
                o[0][ctx.e1.name] == 3
                t1 = 3
            if t2 == 0:
                o[0][ctx.e2.name] == 3
                t2 = 3
            if t1 != 3 or t2 != 3:
                raise TypeMismatchInExpression(ctx)
            return 3
        
        
            
    def visitUnOp(self,ctx:UnOp,o):
        t=self.visit(ctx.e,o)
        if ctx.op == '!':
            if t == 0:
                o[0][ctx.e.name] = 3
                t = 3
            if t != 3:
                raise TypeMismatchInExpression(ctx)
            return 3
        if ctx.op == '-':
            if t == 0:
                o[0][ctx.e.name] = 1
                t = 1
            if t != 1:
                raise TypeMismatchInExpression(ctx)
            return 1
        if ctx.op == '-.':
            if t == 0:
                o[0][ctx.e.name] = 2
                t = 2
            if t != 2:
                raise TypeMismatchInExpression(ctx)
            return 2
        if ctx.op == 'i2f':
            if t == 0:
                o[0][ctx.e.name] = 1
                t = 1
            if t != 1:
                raise TypeMismatchInExpression(ctx)
            return 2
        if ctx.op == 'floor':
            if t == 0:
                o[0][ctx.e.name] == 2
                t = 2
            if t != 2:
                raise TypeMismatchInExpression(ctx)
            return 1

    def visitIntLit(self,ctx,o):
        return 1

    def visitFloatLit(self,ctx,o):
        return 2

    def visitBoolLit(self,ctx,o):
        return 3
        
    def visitId(self,ctx,o):
        for ox in o:
            if type(ox) == tuple:
                if ctx.name in ox[0] and type(ox[0][ctx.name]) != dict:
                    return ox[0][ctx.name]
                if ctx.name in ox[1] and type(ox[1][ctx.name]) != dict:
                    return ox[1][ctx.name]
            else:
                if ctx.name in ox and type(ox[ctx.name]) != dict:
                    return ox[ctx.name]
                    
        raise UndeclaredIdentifier(ctx.name)