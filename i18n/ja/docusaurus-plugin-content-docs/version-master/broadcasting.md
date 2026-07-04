<!-- # Broadcasting -->
# Broadcasting

- [Introduction](#introduction)
- [Quickstart](#quickstart)
- [Server Side Installation](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [Client Side Installation](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [Concept Overview](#concept-overview)
    - [Using an Example Application](#using-example-application)
- [Defining Broadcast Events](#defining-broadcast-events)
    - [Broadcast Name](#broadcast-name)
    - [Broadcast Data](#broadcast-data)
    - [Broadcast Queue](#broadcast-queue)
    - [Broadcast Conditions](#broadcast-conditions)
    - [Broadcasting and Database Transactions](#broadcasting-and-database-transactions)
- [Authorizing Channels](#authorizing-channels)
    - [Defining Authorization Callbacks](#defining-authorization-callbacks)
    - [Defining Channel Classes](#defining-channel-classes)
- [Broadcasting Events](#broadcasting-events)
    - [Only to Others](#only-to-others)
    - [Customizing the Connection](#customizing-the-connection)
    - [Anonymous Events](#anonymous-events)
    - [Rescuing Broadcasts](#rescuing-broadcasts)
- [Receiving Broadcasts](#receiving-broadcasts)
    - [Listening for Events](#listening-for-events)
    - [Leaving a Channel](#leaving-a-channel)
    - [Namespaces](#namespaces)
    - [Using React or Vue](#using-react-or-vue)
- [Presence Channels](#presence-channels)
    - [Authorizing Presence Channels](#authorizing-presence-channels)
    - [Joining Presence Channels](#joining-presence-channels)
    - [Broadcasting to Presence Channels](#broadcasting-to-presence-channels)
- [Model Broadcasting](#model-broadcasting)
    - [Model Broadcasting Conventions](#model-broadcasting-conventions)
    - [Listening for Model Broadcasts](#listening-for-model-broadcasts)
- [Client Events](#client-events)
- [Notifications](#notifications)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In many modern web applications, WebSockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a WebSocket connection to be handled by the client. WebSockets provide a more efficient alternative to continually polling your application's server for data changes that should be reflected in your UI. -->
最新の Web アプリケーションの多くでは、リアルタイムのライブ更新ユーザー インターフェイスを実装するために WebSocket が使用されています。サーバー上で一部のデータが更新されると、通常、メッセージが WebSocket 接続経由で送信され、クライアントによって処理されます。 WebSocket は、UI に反映する必要があるデータ変更をアプリケーションのサーバーに継続的にポーリングするより効率的な代替手段を提供します。

<!-- For example, imagine your application is able to export a user's data to a CSV file and email it to them. However, creating this CSV file takes several minutes so you choose to create and mail the CSV within a [queued job](/docs/master/queues). When the CSV has been created and mailed to the user, we can use event broadcasting to dispatch an `App\Events\UserDataExported` event that is received by our application's JavaScript. Once the event is received, we can display a message to the user that their CSV has been emailed to them without them ever needing to refresh the page. -->
たとえば、アプリケーションがユーザーのデータを CSV ファイルにエクスポートし、電子メールで送信できると想像してください。ただし、この CSV ファイルの作成には数分かかるため、[queued job](/docs/master/queues) 内で CSV を作成してメールで送信することを選択します。 CSV が作成され、ユーザーにメールで送信されたら、イベント ブロードキャストを使用して、アプリケーションの JavaScript が受信する `App\Events\UserDataExported` イベントを送出できます。イベントを受信すると、ページを更新しなくても、CSV が電子メールで送信されたことを示すメッセージをユーザーに表示できます。

<!-- To assist you in building these types of features, Laravel makes it easy to "broadcast" your server-side Laravel [events](/docs/master/events) over a WebSocket connection. Broadcasting your Laravel events allows you to share the same event names and data between your server-side Laravel application and your client-side JavaScript application. -->
この種の機能の構築を支援するために、Laravel では、WebSocket 接続を介してサーバー側 Laravel [events](/docs/master/events) を簡単に「ブロードキャスト」できるようにしています。 Laravel イベントをブロードキャストすると、サーバー側の Laravel アプリケーションとクライアント側の JavaScript アプリケーションの間で同じイベント名とデータを共有できます。

<!-- The core concepts behind broadcasting are simple: clients connect to named channels on the frontend, while your Laravel application broadcasts events to these channels on the backend. These events can contain any additional data you wish to make available to the frontend. -->
ブロードキャストの背後にある中心的な概念は単純です。クライアントはフロントエンドの名前付きチャネルに接続し、Laravel アプリケーションはバックエンドのこれらのチャネルにイベントをブロードキャストします。これらのイベントには、フロントエンドで利用できるようにしたい追加データを含めることができます。

<a name="supported-drivers"></a>
<!-- #### Supported Drivers -->
#### Supported Drivers

<!-- By default, Laravel includes three server-side broadcasting drivers for you to choose from: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com). -->
デフォルトでは、Laravel には、[Laravel Reverb](https://reverb.laravel.com)、[Pusher Channels](https://pusher.com/channels)、および [Ably](https://ably.com) から選択できる 3 つのサーバー側ブロードキャスト ドライバが含まれています。

> [!NOTE]
> イベントブロードキャストに入る前に、[events and listeners](/docs/master/events) にある Laravel のドキュメントを必ず読んでください。

<a name="quickstart"></a>
<!-- ## Quickstart -->
## Quickstart

<!-- By default, broadcasting is not enabled in new Laravel applications. You may enable broadcasting using the `install:broadcasting` Artisan command: -->
デフォルトでは、新しい Laravel アプリケーションではブロードキャストは有効になっていません。 `install:broadcasting` Artisan コマンドを使用してブロードキャストを有効にすることができます。

```shell
php artisan install:broadcasting
```

<!-- The `install:broadcasting` command will prompt you for which event broadcasting service you would like to use. In addition, it will create the `config/broadcasting.php` configuration file and the `routes/channels.php` file where you may register your application's broadcast authorization routes and callbacks. -->
`install:broadcasting` コマンドを実行すると、使用するイベント ブロードキャスト サービスを指定するよう求められます。さらに、アプリケーションのブロードキャスト認可ルートとコールバックを登録できる `config/broadcasting.php` 構成ファイルと `routes/channels.php` ファイルが作成されます。

<!-- Laravel supports several broadcast drivers out of the box: [Laravel Reverb](/docs/master/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), and a `log` driver for local development and debugging. Additionally, a `null` driver is included which allows you to disable broadcasting during testing. A configuration example is included for each of these drivers in the `config/broadcasting.php` configuration file. -->
Laravel は、すぐに使用できるいくつかのブロードキャストドライバ ([Laravel Reverb](/docs/master/reverb)、[Pusher Channels](https://pusher.com/channels)、[Ably](https://ably.com)、ローカル開発およびデバッグ用の `log` ドライバ) をサポートしています。さらに、テスト中にブロードキャストを無効にすることができる `null` ドライバが含まれています。これらの各ドライバの構成例は、`config/broadcasting.php` 構成ファイルに含まれています。

<!-- All of your application's event broadcasting configuration is stored in the `config/broadcasting.php` configuration file. Don't worry if this file does not exist in your application; it will be created when you run the `install:broadcasting` Artisan command. -->
アプリケーションのイベント ブロードキャスト設定はすべて、`config/broadcasting.php` 設定ファイルに保存されます。このファイルがアプリケーションに存在しなくても心配する必要はありません。 `install:broadcasting` Artisan コマンドを実行すると作成されます。

<a name="quickstart-next-steps"></a>
<!-- #### Next Steps -->
#### Next Steps

<!-- Once you have enabled event broadcasting, you're ready to learn more about [defining broadcast events](#defining-broadcast-events) and [listening for events](#listening-for-events). If you're using Laravel's React or Vue [starter kits](/docs/master/starter-kits), you may listen for events using Echo's [useEcho hook](#using-react-or-vue). -->
イベント ブロードキャストを有効にすると、[defining broadcast events](#defining-broadcast-events) と [listening for events](#listening-for-events) について詳しく学ぶことができます。 Laravel の React または Vue [starter kits](/docs/master/starter-kits) を使用している場合は、Echo の [useEcho hook](#using-react-or-vue) を使用してイベントをリッスンできます。

> [!NOTE]
> イベントをブロードキャストする前に、まず [queue worker](/docs/master/queues) を構成して実行する必要があります。すべてのイベント ブロードキャストはキューに入れられたジョブを介して行われるため、ブロードキャストされるイベントによってアプリケーションの応答時間が重大な影響を受けることはありません。

<a name="server-side-installation"></a>
<!-- ## Server Side Installation -->
## Server Side Installation

<!-- To get started using Laravel's event broadcasting, we need to do some configuration within the Laravel application as well as install a few packages. -->
Laravel のイベントブロードキャストの使用を開始するには、Laravel アプリケーション内でいくつかの設定を行い、いくつかのパッケージをインストールする必要があります。

<!-- Event broadcasting is accomplished by a server-side broadcasting driver that broadcasts your Laravel events so that Laravel Echo (a JavaScript library) can receive them within the browser client. Don't worry - we'll walk through each part of the installation process step-by-step. -->
イベントのブロードキャストは、Laravel イベントをブロードキャストするサーバー側ブロードキャスト ドライバによって実現され、Laravel Echo (JavaScript ライブラリ) がブラウザー クライアント内でイベントを受信できるようになります。心配しないでください。インストール プロセスの各部分を段階的に説明します。

<a name="reverb"></a>
<!-- ### Reverb -->
### Reverb

<!-- To quickly enable support for Laravel's broadcasting features while using Reverb as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--reverb` option. This Artisan command will install Reverb's required Composer and NPM packages and update your application's `.env` file with the appropriate variables: -->
イベント ブロードキャスタとして Reverb を使用しているときに Laravel のブロードキャスト機能のサポートをすぐに有効にするには、`--reverb` オプションを指定して `install:broadcasting` Artisan コマンドを呼び出します。この Artisan コマンドは、Reverb に必要な Composer および NPM パッケージをインストールし、アプリケーションの `.env` ファイルを適切な変数で更新します。

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- When running the `install:broadcasting` command, you will be prompted to install [Laravel Reverb](/docs/master/reverb). Of course, you may also install Reverb manually using the Composer package manager: -->
`install:broadcasting` コマンドを実行すると、[Laravel Reverb](/docs/master/reverb) をインストールするように求められます。もちろん、Composer パッケージ マネージャーを使用して Reverb を手動でインストールすることもできます。

```shell
composer require laravel/reverb
```

<!-- Once the package is installed, you may run Reverb's installation command to publish the configuration, add Reverb's required environment variables, and enable event broadcasting in your application: -->
パッケージがインストールされたら、Reverb のインストール コマンドを実行して構成を公開し、Reverb に必要な環境変数を追加して、アプリケーションでのイベント ブロードキャストを有効にすることができます。

```shell
php artisan reverb:install
```

<!-- You can find detailed Reverb installation and usage instructions in the [Reverb documentation](/docs/master/reverb). -->
Reverb のインストールと使用方法の詳細については、[Reverb documentation](/docs/master/reverb) を参照してください。

<a name="pusher-channels"></a>
<!-- ### Pusher Channels -->
### Pusher Channels

<!-- To quickly enable support for Laravel's broadcasting features while using Pusher as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--pusher` option. This Artisan command will prompt you for your Pusher credentials, install the Pusher PHP and JavaScript SDKs, and update your application's `.env` file with the appropriate variables: -->
イベント ブロードキャスタとして Pusher を使用しているときに、Laravel のブロードキャスト機能のサポートをすぐに有効にするには、`--pusher` オプションを指定して `install:broadcasting` Artisan コマンドを呼び出します。この Artisan コマンドは、Pusher 資格情報の入力を求め、Pusher PHP および JavaScript SDK をインストールし、適切な変数を使用してアプリケーションの `.env` ファイルを更新します。

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To install Pusher support manually, you should install the Pusher Channels PHP SDK using the Composer package manager: -->
Pusher サポートを手動でインストールするには、Composer パッケージ マネージャーを使用して Pusher Channels PHP SDK をインストールする必要があります。

```shell
composer require pusher/pusher-php-server
```

<!-- Next, you should configure your Pusher Channels credentials in the `config/broadcasting.php` configuration file. An example Pusher Channels configuration is already included in this file, allowing you to quickly specify your key, secret, and application ID. Typically, you should configure your Pusher Channels credentials in your application's `.env` file: -->
次に、`config/broadcasting.php` 構成ファイルでプッシャー チャネルの資格情報を構成する必要があります。このファイルにはプッシャー チャネル構成の例がすでに含まれており、キー、シークレット、アプリケーション ID をすばやく指定できます。通常、アプリケーションの `.env` ファイルでプッシャー チャネルの資格情報を構成する必要があります。

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

<!-- The `config/broadcasting.php` file's `pusher` configuration also allows you to specify additional `options` that are supported by Channels, such as the cluster. -->
`config/broadcasting.php` ファイルの `pusher` 構成では、クラスターなどのチャネルでサポートされる追加の `options` を指定することもできます。

<!-- Then, set the `BROADCAST_CONNECTION` environment variable to `pusher` in your application's `.env` file: -->
次に、アプリケーションの `.env` ファイルで、`BROADCAST_CONNECTION` 環境変数を `pusher` に設定します。

```ini
BROADCAST_CONNECTION=pusher
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
最後に、クライアント側でブロードキャスト イベントを受信する [Laravel Echo](#client-side-installation) をインストールして構成する準備が整いました。

<a name="ably"></a>
<!-- ### Ably -->
### Ably

> [!NOTE]
> 以下のドキュメントでは、Ably を「プッシャー互換性」モードで使用する方法について説明しています。ただし、Ably チームは、Ably が提供する独自の機能を活用できるブロードキャスタと Echo クライアントを推奨し、維持しています。 Ably が保守するドライバの使用の詳細については、[consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster) を参照してください。

<!-- To quickly enable support for Laravel's broadcasting features while using [Ably](https://ably.com) as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--ably` option. This Artisan command will prompt you for your Ably credentials, install the Ably PHP and JavaScript SDKs, and update your application's `.env` file with the appropriate variables: -->
[Ably](https://ably.com) をイベント ブロードキャスタとして使用しているときに Laravel のブロードキャスト機能のサポートをすぐに有効にするには、`--ably` オプションを指定して `install:broadcasting` Artisan コマンドを呼び出します。この Artisan コマンドは、Ably 認証情報の入力を求め、Ably PHP および JavaScript SDK をインストールし、適切な変数を使用してアプリケーションの `.env` ファイルを更新します。

```shell
php artisan install:broadcasting --ably
```

<!-- **Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.** -->
**続行する前に、Ably アプリケーション設定でプッシャー プロトコルのサポートを有効にする必要があります。 Ably アプリケーションの設定ダッシュボードの「プロトコル アダプター設定」部分でこの機能を有効にすることができます。**

<a name="ably-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To install Ably support manually, you should install the Ably PHP SDK using the Composer package manager: -->
Ably サポートを手動でインストールするには、Composer パッケージ マネージャーを使用して Ably PHP SDK をインストールする必要があります。

```shell
composer require ably/ably-php
```

<!-- Next, you should configure your Ably credentials in the `config/broadcasting.php` configuration file. An example Ably configuration is already included in this file, allowing you to quickly specify your key. Typically, this value should be set via the `ABLY_KEY` [environment variable](/docs/master/configuration#environment-configuration): -->
次に、`config/broadcasting.php` 構成ファイルで Ably 認証情報を構成する必要があります。このファイルには、Ably 構成の例がすでに含まれているため、キーをすばやく指定できます。通常、この値は `ABLY_KEY` [environment variable](/docs/master/configuration#environment-configuration) を介して設定する必要があります。

```ini
ABLY_KEY=your-ably-key
```

<!-- Then, set the `BROADCAST_CONNECTION` environment variable to `ably` in your application's `.env` file: -->
次に、アプリケーションの `.env` ファイルで、`BROADCAST_CONNECTION` 環境変数を `ably` に設定します。

```ini
BROADCAST_CONNECTION=ably
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
最後に、クライアント側でブロードキャスト イベントを受信する [Laravel Echo](#client-side-installation) をインストールして構成する準備が整いました。

<a name="client-side-installation"></a>
<!-- ## Client Side Installation -->
## Client Side Installation

<a name="client-reverb"></a>
<!-- ### Reverb -->
### Reverb

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. -->
[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。

<!-- When installing Laravel Reverb via the `install:broadcasting` Artisan command, Reverb and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below. -->
`install:broadcasting` Artisan コマンドを使用して Laravel Reverb をインストールすると、Reverb と Echo のスキャフォールディングと構成がアプリケーションに自動的に挿入されます。ただし、Laravel Echo を手動で構成したい場合は、以下の手順に従って行うことができます。

<a name="reverb-client-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To manually configure Laravel Echo for your application's frontend, first install the `pusher-js` package since Reverb utilizes the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
アプリケーションのフロントエンド用に Laravel Echo を手動で構成するには、Reverb が WebSocket サブスクリプション、チャネル、およびメッセージにプッシャー プロトコルを利用するため、まず `pusher-js` パッケージをインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework: -->
Echo をインストールすると、アプリケーションの JavaScript で新しい Echo インスタンスを作成できるようになります。これを行うのに最適な場所は、Laravel フレームワークに含まれる `resources/js/bootstrap.js` ファイルの下部です。

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

<!-- Next, you should compile your application's assets: -->
次に、アプリケーションのアセットをコンパイルする必要があります。

```shell
npm run build
```

> [!WARNING]
> Laravel Echo `reverb` ブロードキャスタには、laravel-echo v1.16.0+ が必要です。

<a name="client-pusher-channels"></a>
<!-- ### Pusher Channels -->
### Pusher Channels

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. -->
[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。

<!-- When installing broadcasting support via the `install:broadcasting --pusher` Artisan command, Pusher and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below. -->
`install:broadcasting --pusher` Artisan コマンドを使用してブロードキャスト サポートをインストールすると、Pusher と Echo のスキャフォールディングと構成がアプリケーションに自動的に挿入されます。ただし、Laravel Echo を手動で構成したい場合は、以下の手順に従って行うことができます。

<a name="pusher-client-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
アプリケーションのフロントエンド用に Laravel Echo を手動で構成するには、まず WebSocket サブスクリプション、チャネル、メッセージにプッシャー プロトコルを利用する `laravel-echo` および `pusher-js` パッケージをインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's `resources/js/bootstrap.js` file: -->
Echo がインストールされたら、アプリケーションの `resources/js/bootstrap.js` ファイルに新しい Echo インスタンスを作成する準備が整います。

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

<!-- Next, you should define the appropriate values for the Pusher environment variables in your application's `.env` file. If these variables do not already exist in your `.env` file, you should add them: -->
次に、アプリケーションの `.env` ファイルでプッシャー環境変数の適切な値を定義する必要があります。これらの変数が `.env` ファイルにまだ存在しない場合は、追加する必要があります。

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"

VITE_APP_NAME="${APP_NAME}"
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

<!-- Once you have adjusted the Echo configuration according to your application's needs, you may compile your application's assets: -->
アプリケーションのニーズに応じて Echo 構成を調整したら、アプリケーションのアセットをコンパイルできます。

```shell
npm run build
```

> [!NOTE]
> アプリケーションの JavaScript アセットのコンパイルの詳細については、[Vite](/docs/master/vite) のドキュメントを参照してください。

<a name="using-an-existing-client-instance"></a>
<!-- #### Using an Existing Client Instance -->
#### Using an Existing Client Instance

<!-- If you already have a pre-configured Pusher Channels client instance that you would like Echo to utilize, you may pass it to Echo via the `client` configuration option: -->
Echo で利用したい事前設定済みのプッシャー チャネル クライアント インスタンスがすでにある場合は、`client` 設定オプションを使用してそれを Echo に渡すことができます。

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```

<a name="client-ably"></a>
<!-- ### Ably -->
### Ably

> [!NOTE]
> 以下のドキュメントでは、Ably を「プッシャー互換性」モードで使用する方法について説明しています。ただし、Ably チームは、Ably が提供する独自の機能を活用できるブロードキャスタと Echo クライアントを推奨し、維持しています。 Ably が保守するドライバの使用の詳細については、[consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster) を参照してください。

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. -->
[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。

<!-- When installing broadcasting support via the `install:broadcasting --ably` Artisan command, Ably and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below. -->
`install:broadcasting --ably` Artisan コマンドを使用してブロードキャスト サポートをインストールすると、Ably と Echo のスキャフォールディングと構成がアプリケーションに自動的に挿入されます。ただし、Laravel Echo を手動で構成したい場合は、以下の手順に従って行うことができます。

<a name="ably-client-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
アプリケーションのフロントエンド用に Laravel Echo を手動で構成するには、まず WebSocket サブスクリプション、チャネル、メッセージにプッシャー プロトコルを利用する `laravel-echo` および `pusher-js` パッケージをインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- **Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.** -->
**続行する前に、Ably アプリケーション設定でプッシャー プロトコルのサポートを有効にする必要があります。 Ably アプリケーションの設定ダッシュボードの「プロトコル アダプター設定」部分でこの機能を有効にすることができます。**

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's `resources/js/bootstrap.js` file: -->
Echo がインストールされたら、アプリケーションの `resources/js/bootstrap.js` ファイルに新しい Echo インスタンスを作成する準備が整います。

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

<!-- You may have noticed our Ably Echo configuration references a `VITE_ABLY_PUBLIC_KEY` environment variable. This variable's value should be your Ably public key. Your public key is the portion of your Ably key that occurs before the `:` character. -->
Ably Echo 設定が `VITE_ABLY_PUBLIC_KEY` 環境変数を参照していることに気づいたかもしれません。この変数の値は、Ably 公開キーである必要があります。公開キーは、Ably キーの `:` 文字の前にある部分です。

<!-- Once you have adjusted the Echo configuration according to your needs, you may compile your application's assets: -->
ニーズに応じて Echo 構成を調整したら、アプリケーションのアセットをコンパイルできます。

```shell
npm run dev
```

> [!NOTE]
> アプリケーションの JavaScript アセットのコンパイルの詳細については、[Vite](/docs/master/vite) のドキュメントを参照してください。

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

<!-- Laravel's event broadcasting allows you to broadcast your server-side Laravel events to your client-side JavaScript application using a driver-based approach to WebSockets. Currently, Laravel ships with [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com) drivers. The events may be easily consumed on the client-side using the [Laravel Echo](#client-side-installation) JavaScript package. -->
Laravel のイベント ブロードキャストを使用すると、WebSocket へのドライバベースのアプローチを使用して、サーバー側の Laravel イベントをクライアント側の JavaScript アプリケーションにブロードキャストできます。現在、Laravel には [Laravel Reverb](https://reverb.laravel.com)、[Pusher Channels](https://pusher.com/channels)、および [Ably](https://ably.com) ドライバが同梱されています。イベントは、[Laravel Echo](#client-side-installation) JavaScript パッケージを使用してクライアント側で簡単に使用できます。

<!-- Events are broadcast over "channels", which may be specified as public or private. Any visitor to your application may subscribe to a public channel without any authentication or authorization; however, in order to subscribe to a private channel, a user must be authenticated and authorized to listen on that channel. -->
イベントは、パブリックまたはプライベートとして指定できる「チャネル」を介してブロードキャストされます。アプリケーションへの訪問者は誰でも、認証や許可なしでパブリック チャネルに登録できます。ただし、プライベート チャネルに登録するには、ユーザーが認証され、そのチャネルでリッスンする権限が与えられている必要があります。

<a name="using-example-application"></a>
<!-- ### Using an Example Application -->
### Using an Example Application

<!-- Before diving into each component of event broadcasting, let's take a high level overview using an e-commerce store as an example. -->
イベント ブロードキャストの各コンポーネントに入る前に、電子商取引ストアを例として使用して概要を見てみましょう。

<!-- In our application, let's assume we have a page that allows users to view the shipping status for their orders. Let's also assume that an `OrderShipmentStatusUpdated` event is fired when a shipping status update is processed by the application: -->
このアプリケーションでは、ユーザーが注文の配送ステータスを表示できるページがあると仮定します。また、出荷ステータスの更新がアプリケーションによって処理されるときに、`OrderShipmentStatusUpdated` イベントが発生すると仮定します。

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
<!-- #### The `ShouldBroadcast` Interface -->
#### The `ShouldBroadcast` Interface

<!-- When a user is viewing one of their orders, we don't want them to have to refresh the page to view status updates. Instead, we want to broadcast the updates to the application as they are created. So, we need to mark the `OrderShipmentStatusUpdated` event with the `ShouldBroadcast` interface. This will instruct Laravel to broadcast the event when it is fired: -->
ユーザーが注文の 1 つを表示しているときに、ステータスの更新を表示するためにページを更新する必要がないようにしたいと考えています。代わりに、更新が作成されたときにアプリケーションに更新をブロードキャストしたいと考えています。したがって、`OrderShipmentStatusUpdated` イベントを `ShouldBroadcast` インターフェイスでマークする必要があります。これにより、Laravel がイベントの発生時にイベントをブロードキャストするように指示されます。

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    /**
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

<!-- The `ShouldBroadcast` interface requires our event to define a `broadcastOn` method. This method is responsible for returning the channels that the event should broadcast on. An empty stub of this method is already defined on generated event classes, so we only need to fill in its details. We only want the creator of the order to be able to view status updates, so we will broadcast the event on a private channel that is tied to the order: -->
`ShouldBroadcast` インターフェイスでは、イベントで `broadcastOn` メソッドを定義する必要があります。このメソッドは、イベントがブロードキャストされるチャネルを返す役割を果たします。このメソッドの空のスタブは生成されたイベント クラスですでに定義されているため、その詳細を入力するだけで済みます。注文の作成者のみがステータス更新を表示できるようにしたいため、注文に関連付けられたプライベート チャネルでイベントをブロードキャストします。

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channel the event should broadcast on.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

<!-- If you wish the event to broadcast on multiple channels, you may return an `array` instead: -->
イベントを複数のチャンネルでブロードキャストしたい場合は、代わりに `array` を返すことができます。

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PrivateChannel('orders.'.$this->order->id),
        // ...
    ];
}
```

<a name="example-application-authorizing-channels"></a>
<!-- #### Authorizing Channels -->
#### Authorizing Channels

<!-- Remember, users must be authorized to listen on private channels. We may define our channel authorization rules in our application's `routes/channels.php` file. In this example, we need to verify that any user attempting to listen on the private `orders.1` channel is actually the creator of the order: -->
ユーザーはプライベート チャネルでリッスンすることを許可されている必要があることに注意してください。アプリケーションの `routes/channels.php` ファイルでチャネル認可ルールを定義できます。この例では、プライベート `orders.1` チャネルでリッスンしようとしているユーザーが実際に注文の作成者であることを確認する必要があります。

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

<!-- The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel. -->
`channel` メソッドは、チャネルの名前と、ユーザーがチャネルでリッスンする権限があるかどうかを示す `true` または `false` を返すコールバックの 2 つの引数を受け入れます。

<!-- All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard. -->
すべての認可コールバックは、現在認証されているユーザーを最初の引数として受け取り、追加のワイルドカード パラメーターを後続の引数として受け取ります。この例では、`{orderId}` プレースホルダーを使用して、チャネル名の「ID」部分がワイルドカードであることを示しています。

<a name="listening-for-event-broadcasts"></a>
<!-- #### Listening for Event Broadcasts -->
#### Listening for Event Broadcasts

<!-- Next, all that remains is to listen for the event in our JavaScript application. We can do this using [Laravel Echo](#client-side-installation). Laravel Echo's built-in React and Vue hooks make it simple to get started, and, by default, all of the event's public properties will be included on the broadcast event: -->
次に残っているのは、JavaScript アプリケーションでイベントをリッスンすることだけです。これは、[Laravel Echo](#client-side-installation) を使用して行うことができます。 Laravel Echo に組み込まれている React フックと Vue フックを使用すると、簡単に始めることができます。デフォルトでは、イベントのすべてのパブリック プロパティがブロードキャスト イベントに含まれます。

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<a name="defining-broadcast-events"></a>
<!-- ## Defining Broadcast Events -->
## Defining Broadcast Events

<!-- To inform Laravel that a given event should be broadcast, you must implement the `Illuminate\Contracts\Broadcasting\ShouldBroadcast` interface on the event class. This interface is already imported into all event classes generated by the framework so you may easily add it to any of your events. -->
特定のイベントをブロードキャストする必要があることを Laravel に通知するには、イベント クラスに `Illuminate\Contracts\Broadcasting\ShouldBroadcast` インターフェイスを実装する必要があります。このインターフェイスは、フレームワークによって生成されたすべてのイベント クラスにすでにインポートされているため、任意のイベントに簡単に追加できます。

<!-- The `ShouldBroadcast` interface requires you to implement a single method: `broadcastOn`. The `broadcastOn` method should return a channel or array of channels that the event should broadcast on. The channels should be instances of `Channel`, `PrivateChannel`, or `PresenceChannel`. Instances of `Channel` represent public channels that any user may subscribe to, while `PrivateChannels` and `PresenceChannels` represent private channels that require [channel authorization](#authorizing-channels): -->
`ShouldBroadcast` インターフェイスでは、単一のメソッド `broadcastOn` を実装する必要があります。 `broadcastOn` メソッドは、イベントがブロードキャストされるチャネルまたはチャネルの配列を返す必要があります。チャネルは、`Channel`、`PrivateChannel`、または `PresenceChannel` のインスタンスである必要があります。 `Channel` のインスタンスは、任意のユーザーが購読できるパブリック チャネルを表し、`PrivateChannels` および `PresenceChannels` は、[channel authorization](#authorizing-channels) を必要とするプライベート チャネルを表します。

```php
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.'.$this->user->id),
        ];
    }
}
```

<!-- After implementing the `ShouldBroadcast` interface, you only need to [fire the event](/docs/master/events) as you normally would. Once the event has been fired, a [queued job](/docs/master/queues) will automatically broadcast the event using your specified broadcast driver. -->
`ShouldBroadcast` インターフェイスを実装した後は、通常どおり [fire the event](/docs/master/events) を実行するだけです。イベントが発生すると、[queued job](/docs/master/queues) は指定したブロードキャスト ドライバを使用してイベントを自動的にブロードキャストします。

<a name="broadcast-name"></a>
<!-- ### Broadcast Name -->
### Broadcast Name

<!-- By default, Laravel will broadcast the event using the event's class name. However, you may customize the broadcast name by defining a `broadcastAs` method on the event: -->
デフォルトでは、Laravel はイベントのクラス名を使用してイベントをブロードキャストします。ただし、イベントで `broadcastAs` メソッドを定義することで、ブロードキャスト名をカスタマイズできます。

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

<!-- If you customize the broadcast name using the `broadcastAs` method, you should make sure to register your listener with a leading `.` character. This will instruct Echo to not prepend the application's namespace to the event: -->
`broadcastAs` メソッドを使用してブロードキャスト名をカスタマイズする場合は、先頭に `.` 文字を使用してリスナを登録する必要があります。これにより、アプリケーションの名前空間をイベントの前に付加しないように Echo に指示されます。

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
<!-- ### Broadcast Data -->
### Broadcast Data

<!-- When an event is broadcast, all of its `public` properties are automatically serialized and broadcast as the event's payload, allowing you to access any of its public data from your JavaScript application. So, for example, if your event has a single public `$user` property that contains an Eloquent model, the event's broadcast payload would be: -->
イベントがブロードキャストされると、そのすべての `public` プロパティが自動的にシリアル化され、イベントのペイロードとしてブロードキャストされるため、JavaScript アプリケーションからそのパブリック データのいずれかにアクセスできるようになります。したがって、たとえば、イベントに Eloquent モデルを含む単一のパブリック `$user` プロパティがある場合、イベントのブロードキャスト ペイロードは次のようになります。

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

<!-- However, if you wish to have more fine-grained control over your broadcast payload, you may add a `broadcastWith` method to your event. This method should return the array of data that you wish to broadcast as the event payload: -->
ただし、ブロードキャスト ペイロードをより細かく制御したい場合は、イベントに `broadcastWith` メソッドを追加できます。このメソッドは、イベント ペイロードとしてブロードキャストするデータの配列を返す必要があります。

```php
/**
 * Get the data to broadcast.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(): array
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
<!-- ### Broadcast Queue -->
### Broadcast Queue

<!-- By default, each broadcast event is placed on the default queue for the default queue connection specified in your `queue.php` configuration file. You may customize the queue connection and name used by the broadcaster by using the `Connection` and `Queue` attributes on your event class: -->
デフォルトでは、各ブロードキャスト イベントは、`queue.php` 構成ファイルで指定されたデフォルト キュー接続のデフォルト キューに配置されます。イベント クラスの `Connection` 属性と `Queue` 属性を使用して、ブロードキャスタが使用するキュー接続と名前をカスタマイズできます。

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('redis')]
#[Queue('default')]
class ServerCreated implements ShouldBroadcast
{
    // ...
}
```

<!-- Alternatively, you may customize the queue name by defining a `broadcastQueue` method on your event: -->
あるいは、イベントで `broadcastQueue` メソッドを定義してキュー名をカスタマイズすることもできます。

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

<!-- If you would like to broadcast your event using the `sync` queue instead of the default queue driver, you can implement the `ShouldBroadcastNow` interface instead of `ShouldBroadcast`: -->
デフォルトのキュードライバの代わりに `sync` キューを使用してイベントをブロードキャストする場合は、`ShouldBroadcast` の代わりに `ShouldBroadcastNow` インターフェイスを実装できます。

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
<!-- ### Broadcast Conditions -->
### Broadcast Conditions

<!-- Sometimes you want to broadcast your event only if a given condition is true. You may define these conditions by adding a `broadcastWhen` method to your event class: -->
特定の条件が true の場合にのみイベントをブロードキャストしたい場合があります。これらの条件は、イベント クラスに `broadcastWhen` メソッドを追加することで定義できます。

```php
/**
 * Determine if this event should broadcast.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
<!-- #### Broadcasting and Database Transactions -->
#### Broadcasting and Database Transactions

<!-- When broadcast events are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your event depends on these models, unexpected errors can occur when the job that broadcasts the event is processed. -->
ブロードキャスト イベントがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される場合があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。イベントがこれらのモデルに依存している場合、イベントをブロードキャストするジョブの処理時に予期しないエラーが発生する可能性があります。

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular broadcast event should be dispatched after all open database transactions have been committed by implementing the `ShouldDispatchAfterCommit` interface on the event class: -->
キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、イベント クラスに `ShouldDispatchAfterCommit` インターフェイスを実装することで、開いているすべてのデータベース トランザクションがコミットされた後に特定のブロードキャスト イベントをディスパッチする必要があることを示すことができます。

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
{
    use SerializesModels;
}
```

> [!NOTE]
> これらの問題の回避方法の詳細については、[queued jobs and database transactions](/docs/master/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="authorizing-channels"></a>
<!-- ## Authorizing Channels -->
## Authorizing Channels

<!-- Private channels require you to authorize that the currently authenticated user can actually listen on the channel. This is accomplished by making an HTTP request to your Laravel application with the channel name and allowing your application to determine if the user can listen on that channel. When using [Laravel Echo](#client-side-installation), the HTTP request to authorize subscriptions to private channels will be made automatically. -->
プライベート チャネルでは、現在認証されているユーザーが実際にチャネルをリッスンできることを承認する必要があります。これは、チャンネル名を使用して Laravel アプリケーションに HTTP リクエストを送信し、ユーザーがそのチャンネルでリッスンできるかどうかをアプリケーションが判断できるようにすることで実現されます。 [Laravel Echo](#client-side-installation) を使用すると、プライベート チャネルへのサブスクリプションを承認する HTTP リクエストが自動的に作成されます。

<!-- When broadcasting is installed Laravel attempts to automatically register the `/broadcasting/auth` route to handle authorization requests. If Laravel fails to automatically register these routes, you may register them manually in your application's `/bootstrap/app.php` file: -->
ブロードキャストがインストールされると、Laravel は承認リクエストを処理するために `/broadcasting/auth` ルートを自動的に登録しようとします。 Laravel がこれらのルートを自動的に登録できない場合は、アプリケーションの `/bootstrap/app.php` ファイルに手動で登録できます。

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
<!-- ### Defining Authorization Callbacks -->
### Defining Authorization Callbacks

<!-- Next, we need to define the logic that will actually determine if the currently authenticated user can listen to a given channel. This is done in the `routes/channels.php` file that was created by the `install:broadcasting` Artisan command. In this file, you may use the `Broadcast::channel` method to register channel authorization callbacks: -->
次に、現在認証されているユーザーが特定のチャンネルを聞くことができるかどうかを実際に判断するロジックを定義する必要があります。これは、`install:broadcasting` Artisan コマンドによって作成された `routes/channels.php` ファイルで行われます。このファイルでは、`Broadcast::channel` メソッドを使用してチャネル承認コールバックを登録できます。

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

<!-- The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel. -->
`channel` メソッドは、チャネルの名前と、ユーザーがチャネルでリッスンする権限があるかどうかを示す `true` または `false` を返すコールバックの 2 つの引数を受け入れます。

<!-- All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard. -->
すべての認可コールバックは、現在認証されているユーザーを最初の引数として受け取り、追加のワイルドカード パラメーターを後続の引数として受け取ります。この例では、`{orderId}` プレースホルダーを使用して、チャネル名の「ID」部分がワイルドカードであることを示しています。

<!-- You may view a list of your application's broadcast authorization callbacks using the `channel:list` Artisan command: -->
`channel:list` Artisan コマンドを使用して、アプリケーションのブロードキャスト認可コールバックのリストを表示できます。

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
<!-- #### Authorization Callback Model Binding -->
#### Authorization Callback Model Binding

<!-- Just like HTTP routes, channel routes may also take advantage of implicit and explicit [route model binding](/docs/master/routing#route-model-binding). For example, instead of receiving a string or numeric order ID, you may request an actual `Order` model instance: -->
HTTP ルートと同様に、チャネル ルートも暗黙的および明示的な [route model binding](/docs/master/routing#route-model-binding) を利用できます。たとえば、文字列または数値の注文 ID を受け取る代わりに、実際の `Order` モデル インスタンスをリクエストできます。

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP ルート モデル バインディングとは異なり、チャネル モデル バインディングは自動 [implicit model binding scoping](/docs/master/routing#implicit-model-binding-scoping) をサポートしません。ただし、ほとんどのチャネルは単一モデルの一意の主キーに基づいてスコープを設定できるため、これが問題になることはほとんどありません。

<a name="authorization-callback-authentication"></a>
<!-- #### Authorization Callback Authentication -->
#### Authorization Callback Authentication

<!-- Private and presence broadcast channels authenticate the current user via your application's default authentication guard. If the user is not authenticated, channel authorization is automatically denied and the authorization callback is never executed. However, you may assign multiple, custom guards that should authenticate the incoming request if necessary: -->
プライベート ブロードキャスト チャネルとプレゼンス ブロードキャスト チャネルは、アプリケーションのデフォルトの認証ガードを介して現在のユーザーを認証します。ユーザーが認証されていない場合、チャネル承認は自動的に拒否され、承認コールバックは実行されません。ただし、必要に応じて、受信リクエストを認証する複数のカスタム ガードを割り当てることができます。

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
<!-- ### Defining Channel Classes -->
### Defining Channel Classes

<!-- If your application is consuming many different channels, your `routes/channels.php` file could become bulky. So, instead of using closures to authorize channels, you may use channel classes. To generate a channel class, use the `make:channel` Artisan command. This command will place a new channel class in the `App/Broadcasting` directory. -->
アプリケーションがさまざまなチャネルを使用している場合、`routes/channels.php` ファイルが大きくなる可能性があります。したがって、クロージャを使用してチャネルを承認する代わりに、チャネル クラスを使用することもできます。チャネル クラスを生成するには、`make:channel` Artisan コマンドを使用します。このコマンドは、新しいチャネル クラスを `App/Broadcasting` ディレクトリに配置します。

```shell
php artisan make:channel OrderChannel
```

<!-- Next, register your channel in your `routes/channels.php` file: -->
次に、`routes/channels.php` ファイルにチャンネルを登録します。

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

<!-- Finally, you may place the authorization logic for your channel in the channel class' `join` method. This `join` method will house the same logic you would have typically placed in your channel authorization closure. You may also take advantage of channel model binding: -->
最後に、チャネル クラスの `join` メソッドにチャネルの承認ロジックを配置できます。この `join` メソッドには、通常チャネル承認クロージャに配置するのと同じロジックが格納されます。チャネル モデル バインディングを利用することもできます。

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct() {}

    /**
     * Authenticate the user's access to the channel.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> Laravel の他の多くのクラスと同様に、チャネル クラスは [service container](/docs/master/container) によって自動的に解決されます。したがって、コンストラクターでチャネルに必要な依存関係をタイプヒントで指定できます。

<a name="broadcasting-events"></a>
<!-- ## Broadcasting Events -->
## Broadcasting Events

<!-- Once you have defined an event and marked it with the `ShouldBroadcast` interface, you only need to fire the event using the event's dispatch method. The event dispatcher will notice that the event is marked with the `ShouldBroadcast` interface and will queue the event for broadcasting: -->
イベントを定義し、それを `ShouldBroadcast` インターフェイスでマークしたら、あとはイベントのディスパッチ メソッドを使用してイベントを起動するだけです。イベント ディスパッチャは、イベントが `ShouldBroadcast` インターフェイスでマークされていることを認識し、ブロードキャスト用にイベントをキューに入れます。

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
<!-- ### Only to Others -->
### Only to Others

<!-- When building an application that utilizes event broadcasting, you may occasionally need to broadcast an event to all subscribers to a given channel except for the current user. You may accomplish this using the `broadcast` helper and the `toOthers` method: -->
イベント ブロードキャストを利用するアプリケーションを構築する場合、現在のユーザーを除く特定のチャネルのすべての加入者にイベントをブロードキャストすることが必要になる場合があります。これは、`broadcast` ヘルパと `toOthers` メソッドを使用して実現できます。

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

<!-- To better understand when you may want to use the `toOthers` method, let's imagine a task list application where a user may create a new task by entering a task name. To create a task, your application might make a request to a `/task` URL which broadcasts the task's creation and returns a JSON representation of the new task. When your JavaScript application receives the response from the end-point, it might directly insert the new task into its task list like so: -->
`toOthers` メソッドを使用する必要がある場合をよりよく理解するために、ユーザーがタスク名を入力して新しいタスクを作成できるタスク リスト アプリケーションを想像してみましょう。タスクを作成するために、アプリケーションは、タスクの作成をブロードキャストし、新しいタスクの JSON 表現を返す `/task` URL にリクエストを行うことがあります。 JavaScript アプリケーションがエンドポイントから応答を受け取ると、次のように新しいタスクをタスク リストに直接挿入することがあります。

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

<!-- However, remember that we also broadcast the task's creation. If your JavaScript application is also listening for this event in order to add tasks to the task list, you will have duplicate tasks in your list: one from the end-point and one from the broadcast. You may solve this by using the `toOthers` method to instruct the broadcaster to not broadcast the event to the current user. -->
ただし、タスクの作成もブロードキャストすることに注意してください。タスク リストにタスクを追加するために JavaScript アプリケーションもこのイベントをリッスンしている場合、リストには重複したタスク (エンドポイントからのタスクとブロードキャストからのタスク) が 1 つずつ存在することになります。これを解決するには、`toOthers` メソッドを使用して、現在のユーザーにイベントをブロードキャストしないようにブロードキャスタに指示します。

> [!WARNING]
> `toOthers` メソッドを呼び出すには、イベントで `Illuminate\Broadcasting\InteractsWithSockets` 特性を使用する必要があります。

<a name="only-to-others-configuration"></a>
<!-- #### Configuration -->
#### Configuration

<!-- When you initialize a Laravel Echo instance, a socket ID is assigned to the connection. If you are using a global [Axios](https://github.com/axios/axios) instance to make HTTP requests from your JavaScript application, the socket ID will automatically be attached to every outgoing request as an `X-Socket-ID` header. Then, when you call the `toOthers` method, Laravel will extract the socket ID from the header and instruct the broadcaster to not broadcast to any connections with that socket ID. -->
Laravel Echo インスタンスを初期化すると、接続にソケット ID が割り当てられます。グローバル [Axios](https://github.com/axios/axios) インスタンスを使用して JavaScript アプリケーションから HTTP リクエストを作成している場合、ソケット ID はすべての発信リクエストに `X-Socket-ID` ヘッダーとして自動的に付加されます。次に、`toOthers` メソッドを呼び出すと、Laravel はヘッダーからソケット ID を抽出し、そのソケット ID を持つ接続にブロードキャストしないようにブロードキャスタに指示します。

<!-- If you are not using a global Axios instance, you will need to manually configure your JavaScript application to send the `X-Socket-ID` header with all outgoing requests. You may retrieve the socket ID using the `Echo.socketId` method: -->
グローバル Axios インスタンスを使用していない場合は、すべての送信リクエストで `X-Socket-ID` ヘッダーを送信するように JavaScript アプリケーションを手動で構成する必要があります。 `Echo.socketId` メソッドを使用してソケット ID を取得できます。

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
<!-- ### Customizing the Connection -->
### Customizing the Connection

<!-- If your application interacts with multiple broadcast connections and you want to broadcast an event using a broadcaster other than your default, you may specify which connection to push an event to using the `via` method: -->
アプリケーションが複数のブロードキャスト接続と対話し、デフォルト以外のブロードキャスタを使用してイベントをブロードキャストしたい場合は、`via` メソッドを使用してイベントをプッシュする接続を指定できます。

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

<!-- Alternatively, you may specify the event's broadcast connection by calling the `broadcastVia` method within the event's constructor. However, before doing so, you should ensure that the event class uses the `InteractsWithBroadcasting` trait: -->
あるいは、イベントのコンストラクター内で `broadcastVia` メソッドを呼び出して、イベントのブロードキャスト接続を指定することもできます。ただし、これを行う前に、イベント クラスが `InteractsWithBroadcasting` 特性を使用していることを確認する必要があります。

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithBroadcasting;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    use InteractsWithBroadcasting;

    /**
     * Create a new event instance.
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
<!-- ### Anonymous Events -->
### Anonymous Events

<!-- Sometimes, you may want to broadcast a simple event to your application's frontend without creating a dedicated event class. To accommodate this, the `Broadcast` facade allows you to broadcast "anonymous events": -->
場合によっては、専用のイベント クラスを作成せずに、アプリケーションのフロントエンドに単純なイベントをブロードキャストしたい場合があります。これに対応するために、`Broadcast` ファサードでは「匿名イベント」をブロードキャストできます。

```php
Broadcast::on('orders.'.$order->id)->send();
```

<!-- The example above will broadcast the following event: -->
上記の例では、次のイベントをブロードキャストします。

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

<!-- Using the `as` and `with` methods, you may customize the event's name and data: -->
`as` メソッドと `with` メソッドを使用して、イベントの名前とデータをカスタマイズできます。

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

<!-- The example above will broadcast an event like the following: -->
上記の例では、次のようなイベントをブロードキャストします。

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

<!-- If you would like to broadcast the anonymous event on a private or presence channel, you may utilize the `private` and `presence` methods: -->
匿名イベントをプライベート チャネルまたはプレゼンス チャネルでブロードキャストしたい場合は、`private` メソッドと `presence` メソッドを利用できます。

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

<!-- Broadcasting an anonymous event using the `send` method dispatches the event to your application's [queue](/docs/master/queues) for processing. However, if you would like to broadcast the event immediately, you may use the `sendNow` method: -->
`send` メソッドを使用して匿名イベントをブロードキャストすると、処理のためにイベントがアプリケーションの [queue](/docs/master/queues) にディスパッチされます。ただし、イベントをすぐにブロードキャストしたい場合は、`sendNow` メソッドを使用できます。

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

<!-- To broadcast the event to all channel subscribers except the currently authenticated user, you can invoke the `toOthers` method: -->
現在認証されているユーザーを除くすべてのチャネル加入者にイベントをブロードキャストするには、`toOthers` メソッドを呼び出すことができます。

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
<!-- ### Rescuing Broadcasts -->
### Rescuing Broadcasts

<!-- When your application's queue server is unavailable or Laravel encounters an error while broadcasting an event, an exception is thrown that typically causes the end user to see an application error. Since event broadcasting is often supplementary to your application's core functionality, you can prevent these exceptions from disrupting the user experience by implementing the `ShouldRescue` interface on your events. -->
アプリケーションのキューサーバーが利用できない場合、またはイベントのブロードキャスト中に Laravel でエラーが発生した場合、例外がスローされ、通常はエンドユーザーにアプリケーションエラーが表示されます。イベント ブロードキャストは多くの場合、アプリケーションのコア機能を補足するものであるため、イベントに `ShouldRescue` インターフェイスを実装することで、これらの例外によってユーザー エクスペリエンスが中断されるのを防ぐことができます。

<!-- Events that implement the `ShouldRescue` interface automatically utilize Laravel's [rescue helper function](/docs/master/helpers#method-rescue) during broadcast attempts. This helper catches any exceptions, reports them to your application's exception handler for logging, and allows the application to continue executing normally without interrupting the user's workflow: -->
`ShouldRescue` インターフェイスを実装するイベントは、ブロードキャスト試行中に Laravel の [rescue helper function](/docs/master/helpers#method-rescue) を自動的に利用します。このヘルパは例外をキャッチし、アプリケーションの例外ハンドラーに報告してログを記録し、ユーザーのワークフローを中断することなくアプリケーションが通常どおり実行を継続できるようにします。

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldRescue;

class ServerCreated implements ShouldBroadcast, ShouldRescue
{
    // ...
}
```

<a name="receiving-broadcasts"></a>
<!-- ## Receiving Broadcasts -->
## Receiving Broadcasts

<a name="listening-for-events"></a>
<!-- ### Listening for Events -->
### Listening for Events

<!-- Once you have [installed and instantiated Laravel Echo](#client-side-installation), you are ready to start listening for events that are broadcast from your Laravel application. First, use the `channel` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event: -->
[installed and instantiated Laravel Echo](#client-side-installation) を取得したら、Laravel アプリケーションからブロードキャストされるイベントのリッスンを開始する準備が整います。まず、`channel` メソッドを使用してチャネルのインスタンスを取得し、次に `listen` メソッドを呼び出して指定されたイベントをリッスンします。

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

<!-- If you would like to listen for events on a private channel, use the `private` method instead. You may continue to chain calls to the `listen` method to listen for multiple events on a single channel: -->
プライベート チャネルでイベントをリッスンする場合は、代わりに `private` メソッドを使用してください。 `listen` メソッドへの呼び出しを連鎖して、単一のチャネルで複数のイベントをリッスンすることもできます。

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
<!-- #### Stop Listening for Events -->
#### Stop Listening for Events

<!-- If you would like to stop listening to a given event without [leaving the channel](#leaving-a-channel), you may use the `stopListening` method: -->
[leaving the channel](#leaving-a-channel) を使用せずに特定のイベントのリッスンを停止したい場合は、`stopListening` メソッドを使用できます。

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
<!-- ### Leaving a Channel -->
### Leaving a Channel

<!-- To leave a channel, you may call the `leaveChannel` method on your Echo instance: -->
チャンネルを離れるには、Echo インスタンスで `leaveChannel` メソッドを呼び出します。

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

<!-- If you would like to leave a channel and also its associated private and presence channels, you may call the `leave` method: -->
チャネル、およびそれに関連付けられたプライベート チャネルおよびプレゼンス チャネルから脱退したい場合は、`leave` メソッドを呼び出すことができます。

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
<!-- ### Namespaces -->
### Namespaces

<!-- You may have noticed in the examples above that we did not specify the full `App\Events` namespace for the event classes. This is because Echo will automatically assume the events are located in the `App\Events` namespace. However, you may configure the root namespace when you instantiate Echo by passing a `namespace` configuration option: -->
上記の例で、イベント クラスに完全な `App\Events` 名前空間を指定していないことに気づいたかもしれません。これは、Echo がイベントが `App\Events` 名前空間にあると自動的に想定するためです。ただし、Echo をインスタンス化するときに、`namespace` 構成オプションを渡すことでルート名前空間を構成できます。

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

<!-- Alternatively, you may prefix event classes with a `.` when subscribing to them using Echo. This will allow you to always specify the fully-qualified class name: -->
あるいは、Echo を使用してイベント クラスをサブスクライブするときに、イベント クラスのプレフィックスとして `.` を付けることもできます。これにより、常に完全修飾クラス名を指定できるようになります。

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
<!-- ### Using React or Vue -->
### Using React or Vue

<!-- Laravel Echo includes React and Vue hooks that make it painless to listen for events. To get started, invoke the `useEcho` hook, which is used to listen for private events. The `useEcho` hook will automatically leave channels when the consuming component is unmounted: -->
Laravel Echo には、イベントのリッスンを容易にする React フックと Vue フックが含まれています。まず、プライベート イベントをリッスンするために使用される `useEcho` フックを呼び出します。 `useEcho` フックは、使用側コンポーネントがアンマウントされると自動的にチャネルを離れます。

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<!-- You may listen to multiple events by providing an array of events to `useEcho`: -->
イベントの配列を `useEcho` に提供することで、複数のイベントをリッスンできます。

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

<!-- You may also specify the shape of the broadcast event payload data, providing greater type safety and editing convenience: -->
ブロードキャスト イベント ペイロード データの形式を指定して、タイプ セーフ性と編集の利便性を高めることもできます。

```ts
type OrderData = {
    order: {
        id: number;
        user: {
            id: number;
            name: string;
        };
        created_at: string;
    };
};

useEcho<OrderData>(`orders.${orderId}`, "OrderShipmentStatusUpdated", (e) => {
    console.log(e.order.id);
    console.log(e.order.user.id);
});
```

<!-- The `useEcho` hook will automatically leave channels when the consuming component is unmounted; however, you may utilize the returned functions to manually stop / start listening to channels programmatically when necessary: -->
`useEcho` フックは、使用コンポーネントがアンマウントされると自動的にチャネルを離れます。ただし、必要に応じて、返された関数を利用して、プログラムでチャンネルのリスニングを手動で停止/開始することができます。

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
<!-- #### Connecting to Public Channels -->
#### Connecting to Public Channels

<!-- To connect to a public channel, you may use the `useEchoPublic` hook: -->
パブリック チャネルに接続するには、`useEchoPublic` フックを使用できます。

```js tab=React
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
<!-- #### Connecting to Presence Channels -->
#### Connecting to Presence Channels

<!-- To connect to a presence channel, you may use the `useEchoPresence` hook: -->
プレゼンス チャネルに接続するには、`useEchoPresence` フックを使用できます。

```js tab=React
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connection-status"></a>
<!-- #### Connection Status -->
#### Connection Status

<!-- You may retrieve the current WebSocket connection status using the `useConnectionStatus` hook, which provides reactive status that automatically updates when the connection state changes: -->
`useConnectionStatus` フックを使用して、現在の WebSocket 接続ステータスを取得できます。これにより、接続状態が変化したときに自動的に更新されるリアクティブ ステータスが提供されます。

```js tab=React
import { useConnectionStatus } from "@laravel/echo-react";

function ConnectionIndicator() {
    const status = useConnectionStatus();

    return <div>Connection: {status}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useConnectionStatus } from "@laravel/echo-vue";

const status = useConnectionStatus();
</script>

<template>
    <div>Connection: {{ status }}</div>
</template>
```

<!-- The possible status values are: -->
可能なステータス値は次のとおりです。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `connected` - Successfully connected to the WebSocket server.
- `connecting` - Initial connection attempt in progress.
- `reconnecting` - Attempting to reconnect after a disconnection.
- `disconnected` - Not connected and not attempting to reconnect.
- `failed` - Connection failed and won't retry.
-->
- `connected` - WebSocket サーバーに正常に接続されました。
- `connecting` - 初期接続試行中です。
- `reconnecting` - 切断後に再接続を試みています。
- `disconnected` - 接続されておらず、再接続を試行していません。
- `failed` - 接続に失敗したため、再試行しません。

<!-- </div> -->
</div>

<a name="presence-channels"></a>
<!-- ## Presence Channels -->
## Presence Channels

<!-- Presence channels build on the security of private channels while exposing the additional feature of awareness of who is subscribed to the channel. This makes it easy to build powerful, collaborative application features such as notifying users when another user is viewing the same page or listing the inhabitants of a chat room. -->
プレゼンス チャネルは、プライベート チャネルのセキュリティに基づいて構築されると同時に、誰がチャネルに登録しているかを認識する追加機能を公開します。これにより、別のユーザーが同じページを表示しているときにユーザーに通知したり、チャット ルームの住民をリストしたりするなど、強力な共同アプリケーション機能を簡単に構築できます。

<a name="authorizing-presence-channels"></a>
<!-- ### Authorizing Presence Channels -->
### Authorizing Presence Channels

<!-- All presence channels are also private channels; therefore, users must be [authorized to access them](#authorizing-channels). However, when defining authorization callbacks for presence channels, you will not return `true` if the user is authorized to join the channel. Instead, you should return an array of data about the user. -->
すべてのプレゼンス チャネルはプライベート チャネルでもあります。したがって、ユーザーは [authorized to access them](#authorizing-channels) である必要があります。ただし、プレゼンス チャネルの承認コールバックを定義する場合、ユーザーがチャネルへの参加を承認されている場合は、`true` は返されません。代わりに、ユーザーに関するデータの配列を返す必要があります。

<!-- The data returned by the authorization callback will be made available to the presence channel event listeners in your JavaScript application. If the user is not authorized to join the presence channel, you should return `false` or `null`: -->
承認コールバックによって返されたデータは、JavaScript アプリケーションのプレゼンス チャネル イベント リスナで利用できるようになります。ユーザーがプレゼンス チャネルに参加する権限を持たない場合は、`false` または `null` を返す必要があります。

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
<!-- ### Joining Presence Channels -->
### Joining Presence Channels

<!-- To join a presence channel, you may use Echo's `join` method. The `join` method will return a `PresenceChannel` implementation which, along with exposing the `listen` method, allows you to subscribe to the `here`, `joining`, and `leaving` events. -->
プレゼンス チャネルに参加するには、Echo の `join` メソッドを使用できます。 `join` メソッドは、`PresenceChannel` 実装を返します。これにより、`listen` メソッドが公開されるとともに、`here`、`joining`、および `leaving` イベントをサブスクライブできるようになります。

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // ...
    })
    .joining((user) => {
        console.log(user.name);
    })
    .leaving((user) => {
        console.log(user.name);
    })
    .error((error) => {
        console.error(error);
    });
```

<!-- The `here` callback will be executed immediately once the channel is joined successfully, and will receive an array containing the user information for all of the other users currently subscribed to the channel. The `joining` method will be executed when a new user joins a channel, while the `leaving` method will be executed when a user leaves the channel. The `error` method will be executed when the authentication endpoint returns an HTTP status code other than 200 or if there is a problem parsing the returned JSON. -->
`here` コールバックは、チャネルに正常に参加するとすぐに実行され、現在チャネルに登録している他のすべてのユーザーのユーザー情報を含む配列を受け取ります。 `joining` メソッドは、新しいユーザーがチャンネルに参加するときに実行され、`leaving` メソッドはユーザーがチャンネルを離れるときに実行されます。 `error` メソッドは、認証エンドポイントが 200 以外の HTTP ステータス コードを返した場合、または返された JSON の解析に問題があった場合に実行されます。

<a name="broadcasting-to-presence-channels"></a>
<!-- ### Broadcasting to Presence Channels -->
### Broadcasting to Presence Channels

<!-- Presence channels may receive events just like public or private channels. Using the example of a chatroom, we may want to broadcast `NewMessage` events to the room's presence channel. To do so, we'll return an instance of `PresenceChannel` from the event's `broadcastOn` method: -->
プレゼンス チャネルは、パブリック チャネルまたはプライベート チャネルと同様にイベントを受信できます。チャットルームの例を使用すると、`NewMessage` イベントをルームのプレゼンス チャネルにブロードキャストすることができます。これを行うには、イベントの `broadcastOn` メソッドから `PresenceChannel` のインスタンスを返します。

```php
/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PresenceChannel('chat.'.$this->message->room_id),
    ];
}
```

<!-- As with other events, you may use the `broadcast` helper and the `toOthers` method to exclude the current user from receiving the broadcast: -->
他のイベントと同様に、`broadcast` ヘルパと `toOthers` メソッドを使用して、現在のユーザーをブロードキャストの受信から除外できます。

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

<!-- As typical of other types of events, you may listen for events sent to presence channels using Echo's `listen` method: -->
他のタイプのイベントと同様に、Echo の `listen` メソッドを使用して、プレゼンス チャネルに送信されたイベントをリッスンできます。

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        // ...
    });
```

<a name="model-broadcasting"></a>
<!-- ## Model Broadcasting -->
## Model Broadcasting

> [!WARNING]
> モデルブロードキャストに関する以下のドキュメントを読む前に、Laravel のモデルブロードキャストサービスの一般的な概念とブロードキャストイベントを手動で作成してリッスンする方法を理解しておくことをお勧めします。

<!-- It is common to broadcast events when your application's [Eloquent models](/docs/master/eloquent) are created, updated, or deleted. Of course, this can easily be accomplished by manually [defining custom events for Eloquent model state changes](/docs/master/eloquent#events) and marking those events with the `ShouldBroadcast` interface. -->
アプリケーションの [Eloquent models](/docs/master/eloquent) が作成、更新、または削除されたときにイベントをブロードキャストするのが一般的です。もちろん、これは手動で [defining custom events for Eloquent model state changes](/docs/master/eloquent#events) を実行し、それらのイベントを `ShouldBroadcast` インターフェイスでマークすることで簡単に実現できます。

<!-- However, if you are not using these events for any other purposes in your application, it can be cumbersome to create event classes for the sole purpose of broadcasting them. To remedy this, Laravel allows you to indicate that an Eloquent model should automatically broadcast its state changes. -->
ただし、これらのイベントをアプリケーション内の他の目的で使用していない場合、イベントをブロードキャストすることだけを目的としてイベント クラスを作成するのは面倒になる可能性があります。これを解決するために、Laravel では、Eloquent モデルが状態の変更を自動的にブロードキャストする必要があることを示すことができます。

<!-- To get started, your Eloquent model should use the `Illuminate\Database\Eloquent\BroadcastsEvents` trait. In addition, the model should define a `broadcastOn` method, which will return an array of channels that the model's events should broadcast on: -->
まず、Eloquent モデルで `Illuminate\Database\Eloquent\BroadcastsEvents` トレイトを使用する必要があります。さらに、モデルは `broadcastOn` メソッドを定義する必要があります。これは、モデルのイベントがブロードキャストされるチャネルの配列を返します。

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * Get the user that the post belongs to.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

<!-- Once your model includes this trait and defines its broadcast channels, it will begin automatically broadcasting events when a model instance is created, updated, deleted, trashed, or restored. -->
モデルにこの特性が含まれ、ブロードキャスト チャネルが定義されると、モデル インスタンスが作成、更新、削除、破棄、または復元されたときに、イベントのブロードキャストが自動的に開始されます。

<!-- In addition, you may have noticed that the `broadcastOn` method receives a string `$event` argument. This argument contains the type of event that has occurred on the model and will have a value of `created`, `updated`, `deleted`, `trashed`, or `restored`. By inspecting the value of this variable, you may determine which channels (if any) the model should broadcast to for a particular event: -->
さらに、`broadcastOn` メソッドが文字列 `$event` 引数を受け取ることに気づいたかもしれません。この引数には、モデルで発生したイベントのタイプが含まれ、値は `created`、`updated`、`deleted`、`trashed`、または `restored` になります。この変数の値を検査することで、モデルが特定のイベントに対してどのチャネル (存在する場合) にブロードキャストするかを決定できます。

```php
/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<string, array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>>
 */
public function broadcastOn(string $event): array
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```

<a name="customizing-model-broadcasting-event-creation"></a>
<!-- #### Customizing Model Broadcasting Event Creation -->
#### Customizing Model Broadcasting Event Creation

<!-- Occasionally, you may wish to customize how Laravel creates the underlying model broadcasting event. You may accomplish this by defining a `newBroadcastableEvent` method on your Eloquent model. This method should return an `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` instance: -->
場合によっては、Laravel が基礎となるモデルのブロードキャスト イベントを作成する方法をカスタマイズしたい場合があります。これは、Eloquent モデルで `newBroadcastableEvent` メソッドを定義することで実現できます。このメソッドは `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` インスタンスを返す必要があります。

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * Create a new broadcastable model event for the model.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
<!-- ### Model Broadcasting Conventions -->
### Model Broadcasting Conventions

<a name="model-broadcasting-channel-conventions"></a>
<!-- #### Channel Conventions -->
#### Channel Conventions

<!-- As you may have noticed, the `broadcastOn` method in the model example above did not return `Channel` instances. Instead, Eloquent models were returned directly. If an Eloquent model instance is returned by your model's `broadcastOn` method (or is contained in an array returned by the method), Laravel will automatically instantiate a private channel instance for the model using the model's class name and primary key identifier as the channel name. -->
お気づきかと思いますが、上記のモデル例の `broadcastOn` メソッドは `Channel` インスタンスを返しませんでした。代わりに、Eloquent モデルが直接返されました。 Eloquent モデルインスタンスがモデルの `broadcastOn` メソッドによって返される (またはメソッドによって返される配列に含まれる) 場合、Laravel はモデルのクラス名と主キー識別子をチャネル名として使用して、モデルのプライベートチャネルインスタンスを自動的にインスタンス化します。

<!-- So, an `App\Models\User` model with an `id` of `1` would be converted into an `Illuminate\Broadcasting\PrivateChannel` instance with a name of `App.Models.User.1`. Of course, in addition to returning Eloquent model instances from your model's `broadcastOn` method, you may return complete `Channel` instances in order to have full control over the model's channel names: -->
したがって、`1` の `id` を持つ `App\Models\User` モデルは、`App.Models.User.1` という名前の `Illuminate\Broadcasting\PrivateChannel` インスタンスに変換されます。もちろん、モデルの `broadcastOn` メソッドから Eloquent モデル インスタンスを返すだけでなく、モデルのチャネル名を完全に制御するために完全な `Channel` インスタンスを返すこともできます。

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(string $event): array
{
    return [
        new PrivateChannel('user.'.$this->id)
    ];
}
```

<!-- If you plan to explicitly return a channel instance from your model's `broadcastOn` method, you may pass an Eloquent model instance to the channel's constructor. When doing so, Laravel will use the model channel conventions discussed above to convert the Eloquent model into a channel name string: -->
モデルの `broadcastOn` メソッドからチャネル インスタンスを明示的に返す予定の場合は、Eloquent モデル インスタンスをチャネルのコンストラクターに渡すことができます。その際、Laravel は上で説明したモデル チャネル規則を使用して、Eloquent モデルをチャネル名の文字列に変換します。

```php
return [new Channel($this->user)];
```

<!-- If you need to determine the channel name of a model, you may call the `broadcastChannel` method on any model instance. For example, this method returns the string `App.Models.User.1` for an `App\Models\User` model with an `id` of `1`: -->
モデルのチャネル名を決定する必要がある場合は、任意のモデル インスタンスで `broadcastChannel` メソッドを呼び出すことができます。たとえば、このメソッドは、`1` の `id` を持つ `App\Models\User` モデルの文字列 `App.Models.User.1` を返します。

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
<!-- #### Event Conventions -->
#### Event Conventions

<!-- Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, they are assigned a name and a payload based on conventions. Laravel's convention is to broadcast the event using the class name of the model (not including the namespace) and the name of the model event that triggered the broadcast. -->
モデル ブロードキャスト イベントは、アプリケーションの `App\Events` ディレクトリ内の「実際の」イベントに関連付けられていないため、規則に基づいて名前とペイロードが割り当てられます。 Laravel の規則では、モデルのクラス名 (名前空間は含まない) とブロードキャストをトリガーしたモデル イベントの名前を使用してイベントをブロードキャストします。

<!-- So, for example, an update to the `App\Models\Post` model would broadcast an event to your client-side application as `PostUpdated` with the following payload: -->
したがって、たとえば、`App\Models\Post` モデルを更新すると、次のペイロードを持つ `PostUpdated` としてイベントがクライアント側アプリケーションにブロードキャストされます。

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId"
}
```

<!-- The deletion of the `App\Models\User` model would broadcast an event named `UserDeleted`. -->
`App\Models\User` モデルを削除すると、`UserDeleted` という名前のイベントがブロードキャストされます。

<!-- If you would like, you may define a custom broadcast name and payload by adding a `broadcastAs` and `broadcastWith` method to your model. These methods receive the name of the model event / operation that is occurring, allowing you to customize the event's name and payload for each model operation. If `null` is returned from the `broadcastAs` method, Laravel will use the model broadcasting event name conventions discussed above when broadcasting the event: -->
必要に応じて、`broadcastAs` メソッドと `broadcastWith` メソッドをモデルに追加することで、カスタムのブロードキャスト名とペイロードを定義できます。これらのメソッドは、発生しているモデル イベント/操作の名前を受け取り、モデル操作ごとにイベントの名前とペイロードをカスタマイズできます。 `null` が `broadcastAs` メソッドから返された場合、Laravel はイベントをブロードキャストするときに、上で説明したモデルブロードキャストイベント名規則を使用します。

```php
/**
 * The model event's broadcast name.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(string $event): array
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>
<!-- ### Listening for Model Broadcasts -->
### Listening for Model Broadcasts

<!-- Once you have added the `BroadcastsEvents` trait to your model and defined your model's `broadcastOn` method, you are ready to start listening for broadcasted model events within your client-side application. Before getting started, you may wish to consult the complete documentation on [listening for events](#listening-for-events). -->
`BroadcastsEvents` 特性をモデルに追加し、モデルの `broadcastOn` メソッドを定義したら、クライアント側アプリケーション内でブロードキャストされたモデル イベントのリッスンを開始する準備が整います。始める前に、[listening for events](#listening-for-events) の完全なドキュメントを参照してください。

<!-- First, use the `private` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event. Typically, the channel name given to the `private` method should correspond to Laravel's [model broadcasting conventions](#model-broadcasting-conventions). -->
まず、`private` メソッドを使用してチャネルのインスタンスを取得し、次に `listen` メソッドを呼び出して指定されたイベントをリッスンします。通常、`private` メソッドに指定されるチャネル名は、Laravel の [model broadcasting conventions](#model-broadcasting-conventions) に対応する必要があります。

<!-- Once you have obtained a channel instance, you may use the `listen` method to listen for a particular event. Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, the [event name](#model-broadcasting-event-conventions) must be prefixed with a `.` to indicate it does not belong to a particular namespace. Each model broadcast event has a `model` property which contains all of the broadcastable properties of the model: -->
チャネル インスタンスを取得したら、`listen` メソッドを使用して特定のイベントをリッスンできます。モデル ブロードキャスト イベントは、アプリケーションの `App\Events` ディレクトリ内の「実際の」イベントに関連付けられていないため、特定の名前空間に属していないことを示すために、[event name](#model-broadcasting-event-conventions) の先頭に `.` を付ける必要があります。各モデルのブロードキャスト イベントには、モデルのブロードCastableなプロパティがすべて含まれる `model` プロパティがあります。

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
<!-- #### Using React or Vue -->
#### Using React or Vue

<!-- If you are using React or Vue, you may use Laravel Echo's included `useEchoModel` hook to easily listen for model broadcasts: -->
React または Vue を使用している場合は、Laravel Echo に含まれる `useEchoModel` フックを使用して、モデルのブロードキャストを簡単にリッスンできます。

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

<!-- You may also specify the shape of the model event payload data, providing greater type safety and editing convenience: -->
モデル イベント ペイロード データの形状を指定して、タイプ セーフ性と編集の利便性を高めることもできます。

```ts
type User = {
    id: number;
    name: string;
    email: string;
};

useEchoModel<User, "App.Models.User">("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model.id);
    console.log(e.model.name);
});
```

<a name="client-events"></a>
<!-- ## Client Events -->
## Client Events

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels) を使用する場合、クライアント イベントを送信するには、[application dashboard](https://dashboard.pusher.com/) の [アプリ設定] セクションで [クライアント イベント] オプションを有効にする必要があります。

<!-- Sometimes you may wish to broadcast an event to other connected clients without hitting your Laravel application at all. This can be particularly useful for things like "typing" notifications, where you want to alert users of your application that another user is typing a message on a given screen. -->
Laravel アプリケーションをまったく起動せずに、接続されている他のクライアントにイベントをブロードキャストしたい場合があります。これは、「入力」通知など、別のユーザーが特定の画面でメッセージを入力していることをアプリケーションのユーザーに警告する場合に特に便利です。

<!-- To broadcast client events, you may use Echo's `whisper` method: -->
クライアント イベントをブロードキャストするには、Echo の `whisper` メソッドを使用できます。

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

<!-- To listen for client events, you may use the `listenForWhisper` method: -->
クライアント イベントをリッスンするには、`listenForWhisper` メソッドを使用できます。

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<!-- By pairing event broadcasting with [notifications](/docs/master/notifications), your JavaScript application may receive new notifications as they occur without needing to refresh the page. Before getting started, be sure to read over the documentation on using [the broadcast notification channel](/docs/master/notifications#broadcast-notifications). -->
イベント ブロードキャストと [notifications](/docs/master/notifications) を組み合わせることにより、JavaScript アプリケーションは、ページを更新しなくても、新しい通知が発生したときに受信できるようになります。始める前に、[the broadcast notification channel](/docs/master/notifications#broadcast-notifications) の使用に関するドキュメントを必ずお読みください。

<!-- Once you have configured a notification to use the broadcast channel, you may listen for the broadcast events using Echo's `notification` method. Remember, the channel name should match the class name of the entity receiving the notifications: -->
ブロードキャスト チャネルを使用するように通知を構成したら、Echo の `notification` メソッドを使用してブロードキャスト イベントをリッスンできます。チャネル名は、通知を受信するエンティティのクラス名と一致する必要があることに注意してください。

```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

<!-- In this example, all notifications sent to `App\Models\User` instances via the `broadcast` channel would be received by the callback. A channel authorization callback for the `App.Models.User.{id}` channel is included in your application's `routes/channels.php` file. -->
この例では、`broadcast` チャネル経由で `App\Models\User` インスタンスに送信されたすべての通知がコールバックによって受信されます。 `App.Models.User.{id}` チャネルのチャネル認可コールバックは、アプリケーションの `routes/channels.php` ファイルに含まれています。

<a name="stop-listening-for-notifications"></a>
<!-- #### Stop Listening for Notifications -->
#### Stop Listening for Notifications

<!-- If you would like to stop listening to notifications without [leaving the channel](#leaving-a-channel), you may use the `stopListeningForNotification` method: -->
[leaving the channel](#leaving-a-channel) を使用せずに通知のリスニングを停止したい場合は、`stopListeningForNotification` メソッドを使用できます。

```js
const callback = (notification) => {
    console.log(notification.type);
}

// Start listening...
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// Stop listening (callback must be the same)...
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```

