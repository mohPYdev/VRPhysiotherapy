using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class ObjectInteraction : MonoBehaviour
{
    public XRController controller;


    public void SelectObject()
    {
        // Move the object to the position of the controller
        transform.position = controller.transform.position;
    }


}
