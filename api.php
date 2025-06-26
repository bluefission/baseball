<?php

ini_set('display_errors', 1);
set_time_limit(3000);
date_default_timezone_set('America/New_York');
error_reporting(E_ALL);
$autoloader = require 'vendor/autoload.php';

define('OPUS_ROOT', getcwd());

use \BlueFission\Utils\Loader;
use \BlueFission\Services\Application as App;
use \BlueFission\Services\Service;
use \BlueFission\Services\Request;

// $loader = Loader::instance();
// $loader->addPath(getcwd());

class PlayerService extends Service {
	private $players = [];

	public function __construct() {
		parent::__construct('player');

		$this->players = json_decode('[{"Player name":"B Bonds","position":"LF","Games":2986,"At-bat":9847,"Runs":2227,"Hits":2935,"Double (2B)":601,"third baseman":77,"home run":762,"run batted in":1996,"a walk":2558,"Strikeouts":1539,"stolen base":514,"Caught stealing":141,"AVG":0.298,"On-base Percentage":0.444,"Slugging Percentage":0.607,"On-base Plus Slugging":1.051},{"Player name":"H Aaron","position":"RF","Games":3298,"At-bat":12364,"Runs":2174,"Hits":3771,"Double (2B)":624,"third baseman":98,"home run":755,"run batted in":2297,"a walk":1402,"Strikeouts":1383,"stolen base":240,"Caught stealing":73,"AVG":0.305,"On-base Percentage":0.374,"Slugging Percentage":0.555,"On-base Plus Slugging":0.929},{"Player name":"B Ruth","position":"RF","Games":2504,"At-bat":8399,"Runs":2174,"Hits":2873,"Double (2B)":506,"third baseman":136,"home run":714,"run batted in":2213,"a walk":2062,"Strikeouts":1330,"stolen base":123,"Caught stealing":117,"AVG":0.342,"On-base Percentage":0.474,"Slugging Percentage":0.69,"On-base Plus Slugging":1.164},{"Player name":"A Pujols","position":"1B","Games":3080,"At-bat":11421,"Runs":1914,"Hits":3384,"Double (2B)":686,"third baseman":16,"home run":703,"run batted in":2218,"a walk":1373,"Strikeouts":1404,"stolen base":117,"Caught stealing":43,"AVG":0.296,"On-base Percentage":0.374,"Slugging Percentage":0.544,"On-base Plus Slugging":0.918}]');
	}

	public function getPlayers($data) {
		return json_encode($this->players);
	}

	public function getPlayer($id) {
		if (isset($this->players[$id])) {
			return json_encode($this->players[$id]);
		} else {
			return json_encode(['error' => 'Player not found']);
		}		
	}

	public function updatePlayer($id, $data) {
		if (isset($this->players[$id])) {
			$this->players[$id] = array_merge($this->players[$id], $data);
			return json_encode(['success' => 'Player updated']);
		} else {
			return json_encode(['error' => 'Player not found']);
		}
	}
}

$app = App::instance();
$app->map('get', 'api/players', function() {
	$playerService = new PlayerService();
	$players = $playerService->getPlayers(null);
	die($players);
});
$app->map('get', 'api/player/$id', function($id) {
	$playerService = new PlayerService();
	$player = $playerService->getPlayer($id);
	die($player);
});
$app->map('post', 'api/player/$id', function(Request $request, $id) {
	$data = $request->all();
	die(var_dump($data));
	$playerService = new PlayerService();
	$result = $playerService->updatePlayer($id, $data);
	die($result);
});

$app
->args()
->process()
->run()
;