#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from taupy import * 
    from sympy.abc import a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z
    tau1 = Debate((a&b) >> c, (d&e) >> f)
    pos1 = Position(tau1, {a: True, b: True})
    pos1.is_closed()
    s = Simulation(positions = [{}, {}, {}])
