<?php
// Allow requests from your specific Vue frontend origin
header("Access-Control-Allow-Origin: *"); 
// Allow the necessary HTTP methods (GET, POST, OPTIONS, etc.)
header("Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS");
// Allow the necessary headers (e.g., for authentication)
header("Access-Control-Allow-Headers: Content-Type, Authorization");

ini_set('display_errors', 1);
set_time_limit(3000);
date_default_timezone_set('America/New_York');
error_reporting(E_ALL);
$autoloader = require 'vendor/autoload.php';

// Handle preflight requests (OPTIONS method)
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    header('HTTP/1.1 200 OK');
    exit(0);
}

define('OPUS_ROOT', getcwd());

use \BlueFission\Utils\Loader;
use \BlueFission\Services\Application as App;
use \BlueFission\Services\Service;
use \BlueFission\Services\Request;
use \BlueFission\Connections\Database\MySQLLink;
use \BlueFission\Data\Storage\MySQLBulk;
use \BlueFission\Data\Storage\Storage;
use \BlueFission\Behavioral\Behaviors\State;
use \BlueFission\Str;
use \BlueFission\Connections\Curl;

if(!function_exists('import_env_vars')) {
	function import_env_vars( $file ) {
		$variables = file($file);
		foreach ($variables as $var) {
			putenv(trim($var));
			list($name, $value) = explode("=", $var);
			$_ENV[$name] = $value;
		}
	}
}

if(!function_exists('env')) {
  function env($key, $default = null)
  {
      $value = getenv($key);

      if ($value === false) {
          return $default;
      }
      return $value;
  }
}

// Load environment variables from .env file
$envFile = OPUS_ROOT . '/.env';
if (file_exists($envFile)) {
	import_env_vars($envFile);
} else {
	die("Environment file not found: $envFile");
}

// $loader = Loader::instance();
// $loader->addPath(getcwd());

$config = [
	'target'=>env('MYSQL_DB_HOST', 'localhost'),
	'username'=>env('MYSQL_DB_USERNAME'),
	'password'=>env('MYSQL_DB_PASSWORD'),
	'database'=>env('MYSQL_DB_NAME'),
	'port'=>env('MYSQL_DB_PORT'),
	'table'=>'',
	'key'=>'_rowid',
	'ignore_null'=>false,
];
$link = new MySQLLink($config);
$link->open();

$model = new MySQLBulk([
	'location'=>$config['database'],
	'name'=>'players',
	'fields'=>[],
	'auto_join'=>false,
	'ignore_null'=>true,
	'save_related_tables'=>false,
]);

class PlayerService extends Service {
	private $players = [];
	private $model;
	private $curl;

	public function __construct(Storage $model) {
		parent::__construct();

		$this->model = $model;
		$this->model->activate();

		///////////////////////////////////////////////////////
		// Uncomment what's below to initialize the database //
		///////////////////////////////////////////////////////

		// $fields = $this->model->fields();
		// $row = $this->model->limit(1)->read()->result()->first();

		// if (count($fields) == 0 || !$row) {
		// 	// Load players from the api
		// 	$response = file_get_contents('https://api.hirefraction.com/api/test/baseball');
		// 	$players = json_decode($response, true);

		// 	$firstPlayer = $players[0] ?? null;
		// 	$this->model->perform( State::DRAFT );
		// 	$fields = [];
		// 	foreach ($firstPlayer as $k=>$v) {
		// 		$fields[Str::replace(Str::slugify($k), '-', '_')] = [];
		// 	}
		// 	$tables['players'] = $fields;
		// 	$this->model->config('fields', $tables);
		// 	if (is_array($players) && count($players) > 0) {

		// 		// Set the fields based on the first player's data
		// 		foreach ($players as $player) {
		// 			// die(var_dump($firstPlayer));
		// 			$this->model->clear();
		// 			foreach ($player as $field => $value) {
		// 				// Convert field names to lowercase and replace spaces with underscores
		// 				$cleanField = Str::replace(Str::slugify($field), '-', '_');
		// 				$this->model->field($cleanField, $value);
		// 			}
		// 			$this->model->write();
		// 		}
		// 	} else {
		// 		die("Failed to load players from the API.");
		// 	}
		// 	$this->model->halt( State::DRAFT );
		// }
		$this->model->clear();
		$this->model->limit(0, 1000);

		$this->curl = new Curl([
        'method' => 'post',
    ]);

    $headers = [
        'Content-Type: application/json'
    ];

    $this->curl->config('headers', $headers);
    $this->curl->config('target', 'http://localhost:5000/summary');
    $this->curl->config('verbose', true);
	}

	public function getPlayers($data) {
		$this->model->order('hits', 'desc');
		$this->players = $this->model->read()->result();

		return json_encode($this->players->toArray());
	}

	public function getPlayer($id) {
		$this->model->player_id = $id;
		$player = $this->model->read()->result()->first();
		if (isset($player)) {
			if (!isset($player->notes) || empty($player->notes)) {
				// Generate notes if not already present
				$player->notes = $this->generateNotes($player);
				$this->updatePlayer($id, $player->data());
			}
			return json_encode($player->data());
		} else {
			return json_encode(['error' => 'Player not found']);
		}		
	}

	public function updatePlayer($id, $data) {
		$this->model->clear();
		$this->model->player_id = $id;
		$player = $this->model->read()->result()->first();
		if (isset($player)) {
			$this->model->assign($data);
			$this->model->write();
			return json_encode(['success' => $this->model->status()]);
		} else {
			return json_encode(['error' => 'Player not found']);
		}
	}

	private function generateNotes($player)
	{
		$prompt = "Regard the following player's statistics:\n";
		foreach ($player->data() as $key => $value) {
			$prompt .= ucfirst($key) . ": " . $value . "\n";
		}

		$request_data = [
      'prompt' => $prompt,
    ];
    
		$this->curl->open();
    $this->curl->query($request_data);
    $response = $this->curl->result();
    $this->curl->close();

    $result = json_decode($response, true);

    $output = "Summary: " . ($result['summary'] ?? 'No summary available') . "\n";
    $output .= "Strengths: " . ($result['strengths'] ?? 'No strengths available') . "\n";
    $output .= "Weaknesses: " . ($result['weaknesses'] ?? 'No weaknesses available') . "\n";
    $output .= "Suggestions: " . ($result['strategy'] ?? 'No suggestions available') . "\n";
		
		return $output;
	}
}


// Actual application
$service = new PlayerService($model);

$app = App::instance();
$app->map('get', 'api/players', function() use ($service) {
	$players = $service->getPlayers(null);
	die($players);
});
$app->map('get', 'api/player/$id', function($id) use ($service) {
	$player = $service->getPlayer($id);
	die($player);
});
$app->map('put', 'api/player/$id', function(Request $request, $id) use ($service) {
	$data = $request->all();
	$result = $service->updatePlayer($id, $data);
	die($result);
});

$app
->args()
->process()
->run()
;