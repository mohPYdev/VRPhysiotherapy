using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LeftAvatarControl : MonoBehaviour
{
    public GameObject right_avatar;
    public GameObject left_avatar;

    public void OnAnimationFinish()
    {
        //SceneManager.LoadSceneAsync(1);
        left_avatar.gameObject.SetActive(false);
        right_avatar.gameObject.SetActive(true);
    }
}
