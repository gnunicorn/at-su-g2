<?php
/*
Plugin Name: SSO
Plugin URI: http://login.sourcefabric.org
Description: SSO
Author: Andrey Podshivalov
Version: 1.0
Author URI: http://login.sourcefabric.org
*/

function sso_logout()
{
    include_once('conf.sso.php');
    header('Location: '. $ini['SSO_SERVER_LOGOUT_URL']);
    exit();
}

function sso_login()
{
    // check for logged user
    $user = wp_get_current_user();
    if ($user->ID != 0 ) {
        $redirect_to = admin_url();
        wp_safe_redirect($redirect_to);
        exit();
    }

    include_once('conf.sso.php');
    if (empty($_REQUEST[$ini['SSO_TOKEN_NAME']])) {
        header('Location: '. $ini['SSO_SERVER_LOGIN_URL'] . '?return='
            . urlencode($ini['SSO_RETURN_URL']));
        exit(0);
    } else {
        $ch = curl_init();
        $url = $ini['SSO_SERVER_CHECK_URL'] . '?' . $ini['SSO_TOKEN_NAME']
            . '=' . $_GET[$ini['SSO_TOKEN_NAME']]
            . '&remote_addr=' . $_SERVER['REMOTE_ADDR'];
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 15);
        curl_setopt($ch, CURLOPT_TIMEOUT, 15);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 1);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 1);
        curl_setopt($ch, CURLOPT_CAPATH, $ini['SSO_SSL_CA_PATH']);
        curl_setopt($ch, CURLOPT_CAINFO, $ini['SSO_SSL_CA_CERT']);
        curl_setopt($ch, CURLOPT_SSLCERT, $ini['SSO_SSL_CERT']);
        curl_setopt($ch, CURLOPT_SSLKEY, $ini['SSO_SSL_KEY']);

        $result = curl_exec($ch);
        $sso = @unserialize($result);
        if (!empty($sso['login'])) {

            // do login
            $login = $sso['login'];
            if ($user = get_userdatabylogin($login)) {
                $uid = $user->ID;
            } else {
                require_once ABSPATH . '/wp-includes/registration.php';
                if (email_exists($sso['email'])) {
                    wp_die(sprintf(/*WP_I18N_NO_CONFIG*/"You can not register: email address exists."/*/WP_I18N_NO_CONFIG*/, $path), /*WP_I18N_ERROR_TITLE*/"WordPress &rsaquo; Error"/*/WP_I18N_ERROR_TITLE*/, array('text_direction' => $text_direction));
                }
                // new user
                $user_data = array(
                    'user_login' => $login,
                    'user_pass' => wp_generate_password(),
                    'user_email' => $sso['email'],
                    'user_nicename' => $sso['name'],
                    'nickname' => $sso['name'],
                    'display_name' => $sso['name'],
                );
                $uid = wp_insert_user($user_data);
            }
            wp_set_auth_cookie($uid, true, false);
            wp_set_current_user($uid);
            $redirect_to = admin_url();
            wp_safe_redirect($redirect_to);
            exit();
        }

        // wrong sso authentication
        wp_die(sprintf(/*WP_I18N_NO_CONFIG*/"There is a wrong SSO authentication. Please ask administrator."/*/WP_I18N_NO_CONFIG*/, $path), /*WP_I18N_ERROR_TITLE*/"WordPress &rsaquo; Error"/*/WP_I18N_ERROR_TITLE*/, array('text_direction' => $text_direction));
    }
}

add_action('login_form_login', 'sso_login');
add_action('wp_logout', 'sso_logout');

?>