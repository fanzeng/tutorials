/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edu.princeton.cs.algs4;

/**
 *
 * @author fzeng
 */

public class Cat_1{
    public static void main(String[] args){
        Out out = new Out(args[args.length-1]);
        for (int i = 0; i < args.length - 1; i++) {
            In in  = new In(args[i]);
            String s = in.readAll();
            out.println(s);
            in.close();
        }
        out.close();

    }
}