using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class movementCube : MonoBehaviour
{

    void Update()
    {
        float radius = 6f;

        // Calculate the distance from the object to the origin
        float distance = Mathf.Sqrt(Mathf.Pow((transform.position.x - 11.5f) , 2) + Mathf.Pow(transform.position.y - 0.49f , 2));
        distance = Mathf.Round(distance * 100) / 100;

        print(distance);

        // If the object is not on the circumference of the circle, reposition it
        if (distance != radius)
        {
            // Calculate the new y position on the circumference of the circle
            float newY = Mathf.Sqrt(Mathf.Pow(radius, 2) - Mathf.Pow(transform.position.x, 2));

            print(newY);

            // Update the position
            transform.position = new Vector3(transform.position.x, newY, transform.position.z);
        }
    }
}
