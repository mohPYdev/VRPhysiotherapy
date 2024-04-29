using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollisionCube : MonoBehaviour
{
    public GameObject test;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnTriggerEnter(Collider other)
    {
        test.SetActive(true);
    }

    void OnTriggerStay(Collider other)
    {
        
    }

    void OnTriggerExit(Collider other)
    {
        test.SetActive(false);
    }


    public void start_collision()
    {
        test.SetActive(true);
    }

    public void stop_collision()
    {
        test.SetActive(false);
    }
}
