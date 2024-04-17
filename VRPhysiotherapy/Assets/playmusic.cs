using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class playmusic : MonoBehaviour
{
    public void PlayButton()
    {
        AudioManager.instance.PlaySFX("Click_Button");
    }
}
