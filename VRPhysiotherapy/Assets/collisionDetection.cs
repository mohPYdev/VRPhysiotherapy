using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class collisionDetection : MonoBehaviour
{
    public GameObject cube; // Reference to the cube's transform
    public Vector3 targetPosition; // Specific position to move the cube to

    // This method is called when a collision is detected
    private void OnCollisionEnter(Collision collision)
    {
        // Check if the collision involves the GameObject with the specific tag
        if (collision.gameObject.CompareTag("CubeCollider"))
        {
            // Move the cube to the target position
            cube.transform.position = targetPosition;
        }
    }
}
