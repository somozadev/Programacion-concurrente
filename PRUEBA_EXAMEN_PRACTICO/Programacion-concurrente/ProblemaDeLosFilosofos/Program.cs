using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;

namespace ProblemaDeLosFilosofos
{
    class Program
    {
        static void Main(string[] args)
        {
            const int numPhil = 5;
            Philosopher[] philosophers = new Philosopher[numPhil];
            
            for(int i = 0; i < numPhil; i++)
            {
                philosophers[i] = new Philosopher(i+1,new Fork(0), new Fork(1));
                philosophers[i].philoThread = new Thread(philosophers[i].Eat);
                philosophers[i].philoThread.Start();

            }

            
        }
    }

    public class Fork
    {
        private int id;
        private bool free;

        public Fork(int id)
        {
            this.id = id;
            free = true;
        }

        public void TakeRight(int _id)
        {
            while(!free)
            {
                // this.wait();
                Console.WriteLine("Phylosopher {0} picks the right fork {1}", _id, id);
                free = false;
            }
        }
        public bool TakeLeft(int _id)
        {
            while(!free)
            {
                Random rnd = new Random();
                // this.wait(rnd.Next(1000)+500);
                return false;
            }
            Console.WriteLine("Phylosopher {0} picks the left fork {1}", _id, id);
            free = false;
            return true;
            
        }

        public void Drop(int _id)
        {
            free = true;
            Console.WriteLine("Phylosopher {0} drops the fork {1}", _id, id);
            //this.notify();
            
        }

    }

    public class Philosopher 
    {
        public Thread philoThread;
        private int id;
        private Fork left,right;


        public Philosopher(int id, Fork left, Fork right)
        {
            this.id = id;
            this.left = left;
            this.right = right;
        }

        public void Start()
        {
        }

        public void Eat()
        {
            right.TakeRight(id);
        }

    }





}
