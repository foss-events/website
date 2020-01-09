<?php
/*
* SPDX-FileCopyrightText: 2019 Free Software Foundation Europe e.V. <https://fsfe.org>
* SPDX-FileCopyrightText: 2018 Daniel Martin Gomez
* SPDX-License-Identifier: AGPL-3.0-or-later
*
* share-buttons: Share buttons for many social networks and services
* Upstream: https://git.fsfe.org/FSFE/share-buttons
*/

// Change these variables
$fediverseuser = "@FOSS_events@mastodon.social";
$diasporauser = "";
$twitteruser = "FOSS_events";
$flattruser = "";
$supporturl = "https://foss.events/#contribute";

// Don't change below here
$service = isset($_GET['service']) ? $_GET['service'] : false;
$url = isset($_GET['url']) ? $_GET['url'] : false;
$title = isset($_GET['title']) ? $_GET['title'] : false;
$ref = isset($_GET['ref']) ? $_GET['ref'] : false;
$fediversepod = isset($_GET['fediversepod']) ? $_GET['fediversepod'] : false;

if(empty($service) || empty($url)) {
  echo 'At least one required variable is empty. You have to define at least service and url';
} else {
  $service = htmlspecialchars($service);
  $fediversepod = htmlspecialchars($fediversepod);
  $url = urlencode($url);
  $title = urlencode($title);

  /* Special referrers for FSFE campaigns */
  if($ref == "pmpc-side" || $ref == "pmpc-spread") {
    $via_fed = "";
    $via_tw = "";
    $via_dia = "";
    $supporturl = "https://fsfe.org/donate?pmpc";
  } else {
    $via_fed = " via " . $fediverseuser;
    $via_tw = "&via=" . $twitteruser;
    $via_dia = " via " . $diasporauser;
  }

  if ($service === "fediverse") {
    $fediversepod = validateurl($fediversepod);
    $fediverse = which_fediverse($fediversepod);
    if($fediverse === "mastodon") {
      // Mastodon
      header("Location: " . $fediversepod . "/share?text=" . $title . " " . $url . $via_fed);
    } elseif($fediverse === "diaspora") {
      // Diaspora
      header("Location: " . $fediversepod . "/bookmarklet?url=" . $url . "&title=" . $title . $via_dia);
    } elseif($fediverse === "gnusocial") {
      // GNU Social
      header("Location: " . $fediversepod . "/notice/new?status_textarea=" . $title . " " . $url . $via_fed);
    } else {
      echo 'Your Fediverse instance is unknown. We cannot find out which service it belongs to, sorry.';
    }
    die();
  } elseif($service === "reddit") {
    header("Location: https://reddit.com/submit?url=" . $url . "&title=" . $title);
    die();
  } elseif($service === "flattr") {
    header("Location: https://flattr.com/submit/auto?user_id=" . $flattruser . "&url=" . $url . "&title=" . $title);
    die();
  } elseif($service === "hnews") {
    header("Location: https://news.ycombinator.com/submitlink?u=" . $url . "&t=" . $title);
    die();
  } elseif($service === "twitter") {
    header("Location: https://twitter.com/share?url=" . $url . "&text=" . $title . $via_tw);
    die();
  } elseif($service === "facebook") {
    header("Location: https://www.facebook.com/sharer/sharer.php?u=" . $url);
    die();
  } elseif($service === "gplus") {
    header("Location: https://plus.google.com/share?url=" . $url);
    die();
  } elseif($service === "support") {
    header("Location: " . $supporturl);
    die();
  } else {
    echo 'Social network unknown.';
  }
}

// Sanitise URLs
function validateurl($url) {
  // If Fediverse pod has been typed without http(s):// prefix, add it
  if (preg_match('#^https?://#i', $url) === 0) {
    $url = 'https://' . $url;
  }
  // remove trailing spaces and slashes
  $url = trim($url, " /");

  return $url;
}

// Is $pod a Mastodon instance or a GNU Social server?
function getFediverseNetwork($pod) {
$curl = curl_init($pod . "/api/statusnet/version.xml");
curl_exec($curl);
$code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);
if ($code == 200) {
  // GNU social server
  return 0;
} else {
  // Mastodon server
  return 1;
}
}

function which_fediverse($pod) {
  if (check_httpstatus($pod . "/api/v1/instance")) {
    // Mastodon
    return "mastodon";
  } elseif (check_httpstatus($pod . "/api/statusnet/version.xml")) {
    // GNU social
    return "gnusocial";
  } elseif (check_httpstatus($pod . "/users/sign_in")) {
    // Diaspora
    return "diaspora";
  } else {
    return "none";
  }
}

function check_httpstatus($url) {
  $headers = get_headers($url, 1);
  // check up to 2 redirections
  if (array_key_exists('2', $headers)) {
    $httpstatus = $headers[2];
  } elseif (array_key_exists('1', $headers)) {
    $httpstatus = $headers[1];
  } else {
    $httpstatus = $headers[0];
  }
  // check if HTTP status is 200
  if (strpos($httpstatus, '200 OK') !== false) {
    return true;
  } else {
    return false;
  }
}

?>
