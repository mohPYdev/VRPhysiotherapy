using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class changeobjectpositin : MonoBehaviour
{
    public static GameObject game;

    public GameObject left_position;
    public GameObject right_position;
    public GameObject xr_org;

    static int i = 0;



    public void start_move()
    {
        if (i == 1)
        {

            SocketClient sc = xr_org.GetComponent<SocketClient>();
            sc.start_movement();
            i++;
        }
    }

    public void end_move()
    {
        if (i == 2)
        {
            SocketClient sc = xr_org.GetComponent<SocketClient>();
            sc.end_movement();
            i = 0;
        }

    }



    public static void gameobject_set(GameObject g)
    {


        game = g;
        if (i == 0)
        {
            i++;
        }

        
        
    }
    public void location_left()
    {
        
        game.transform.position = left_position.transform.position;
 
    }
    public void location_right()
    {
        game.transform.position = right_position.transform.position;
    }

   

}
