<!-- # Broadcasting -->
# Broadcasting

- [Introduction](#introduction)
- [Server Side Installation](#server-side-installation)
    - [Configuration](#configuration)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [Open Source Alternatives](#open-source-alternatives)
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
    - [Defining Authorization Routes](#defining-authorization-routes)
    - [Defining Authorization Callbacks](#defining-authorization-callbacks)
    - [Defining Channel Classes](#defining-channel-classes)
- [Broadcasting Events](#broadcasting-events)
    - [Only to Others](#only-to-others)
    - [Customizing the Connection](#customizing-the-connection)
- [Receiving Broadcasts](#receiving-broadcasts)
    - [Listening for Events](#listening-for-events)
    - [Leaving a Channel](#leaving-a-channel)
    - [Namespaces](#namespaces)
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

<!-- For example, imagine your application is able to export a user's data to a CSV file and email it to them. However, creating this CSV file takes several minutes so you choose to create and mail the CSV within a [queued job](/docs/10.x/queues). When the CSV has been created and mailed to the user, we can use event broadcasting to dispatch an `App\Events\UserDataExported` event that is received by our application's JavaScript. Once the event is received, we can display a message to the user that their CSV has been emailed to them without them ever needing to refresh the page. -->
たとえば、アプリケーションがユーザーのデータを CSV ファイルにエクスポートし、電子メールで送信できると想像してください。ただし、この CSV ファイルの作成には数分かかるため、[queued job](/docs/10.x/queues) 内で CSV を作成してメールで送信することを選択します。 CSV が作成され、ユーザーにメールで送信されたら、イベント ブロードキャストを使用して、アプリケーションの JavaScript が受信する `App\Events\UserDataExported` イベントを送出できます。イベントを受信すると、ページを更新しなくても、CSV が電子メールで送信されたことを示すメッセージをユーザーに表示できます。

<!-- To assist you in building these types of features, Laravel makes it easy to "broadcast" your server-side Laravel [events](/docs/10.x/events) over a WebSocket connection. Broadcasting your Laravel events allows you to share the same event names and data between your server-side Laravel application and your client-side JavaScript application. -->
この種の機能の構築を支援するために、Laravel では、WebSocket 接続を介してサーバー側 Laravel [events](/docs/10.x/events) を簡単に「ブロードキャスト」できるようにしています。 Laravel イベントをブロードキャストすると、サーバー側の Laravel アプリケーションとクライアント側の JavaScript アプリケーションの間で同じイベント名とデータを共有できます。

<!-- The core concepts behind broadcasting are simple: clients connect to named channels on the frontend, while your Laravel application broadcasts events to these channels on the backend. These events can contain any additional data you wish to make available to the frontend. -->
ブロードキャストの背後にある中心的な概念は単純です。クライアントはフロントエンドの名前付きチャネルに接続し、Laravel アプリケーションはバックエンドのこれらのチャネルにイベントをブロードキャストします。これらのイベントには、フロントエンドで利用できるようにしたい追加データを含めることができます。

<a name="supported-drivers"></a>
<!-- #### Supported Drivers -->
#### Supported Drivers

<!-- By default, Laravel includes three server-side broadcasting drivers for you to choose from: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com). -->
デフォルトでは、Laravel には、[Laravel Reverb](https://reverb.laravel.com)、[Pusher Channels](https://pusher.com/channels)、および [Ably](https://ably.com) から選択できる 3 つのサーバー側ブロードキャスト ドライバが含まれています。

> [!NOTE]
> イベントブロードキャストに入る前に、[events and listeners](/docs/10.x/events) にある Laravel のドキュメントを必ず読んでください。

<a name="server-side-installation"></a>
<!-- ## Server Side Installation -->
## Server Side Installation

<!-- To get started using Laravel's event broadcasting, we need to do some configuration within the Laravel application as well as install a few packages. -->
Laravel のイベントブロードキャストの使用を開始するには、Laravel アプリケーション内でいくつかの設定を行い、いくつかのパッケージをインストールする必要があります。

<!-- Event broadcasting is accomplished by a server-side broadcasting driver that broadcasts your Laravel events so that Laravel Echo (a JavaScript library) can receive them within the browser client. Don't worry - we'll walk through each part of the installation process step-by-step. -->
イベントのブロードキャストは、Laravel イベントをブロードキャストするサーバー側ブロードキャスト ドライバによって実現され、Laravel Echo (JavaScript ライブラリ) がブラウザー クライアント内でイベントを受信できるようになります。心配しないでください。インストール プロセスの各部分を段階的に説明します。

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- All of your application's event broadcasting configuration is stored in the `config/broadcasting.php` configuration file. Laravel supports several broadcast drivers out of the box: [Pusher Channels](https://pusher.com/channels), [Redis](/docs/10.x/redis), and a `log` driver for local development and debugging. Additionally, a `null` driver is included which allows you to totally disable broadcasting during testing. A configuration example is included for each of these drivers in the `config/broadcasting.php` configuration file. -->
アプリケーションのイベント ブロードキャスト設定はすべて、`config/broadcasting.php` 設定ファイルに保存されます。 Laravel は、すぐに使用できるいくつかのブロードキャスト ドライバ (ローカル開発およびデバッグ用の [Pusher Channels](https://pusher.com/channels)、[Redis](/docs/10.x/redis)、および `log` ドライバ) をサポートしています。さらに、テスト中にブロードキャストを完全に無効にすることができる `null` ドライバが含まれています。これらの各ドライバの構成例は、`config/broadcasting.php` 構成ファイルに含まれています。

<a name="broadcast-service-provider"></a>
<!-- #### Broadcast Service Provider -->
#### Broadcast Service Provider

<!-- Before broadcasting any events, you will first need to register the `App\Providers\BroadcastServiceProvider`. In new Laravel applications, you only need to uncomment this provider in the `providers` array of your `config/app.php` configuration file. This `BroadcastServiceProvider` contains the code necessary to register the broadcast authorization routes and callbacks. -->
イベントをブロードキャストする前に、まず `App\Providers\BroadcastServiceProvider` を登録する必要があります。新しい Laravel アプリケーションでは、`config/app.php` 構成ファイルの `providers` 配列でこのプロバイダのコメントを解除するだけで済みます。この `BroadcastServiceProvider` には、ブロードキャスト認可ルートとコールバックを登録するために必要なコードが含まれています。

<a name="queue-configuration"></a>
<!-- #### Queue Configuration -->
#### Queue Configuration

<!-- You will also need to configure and run a [queue worker](/docs/10.x/queues). All event broadcasting is done via queued jobs so that the response time of your application is not seriously affected by events being broadcast. -->
[queue worker](/docs/10.x/queues) を構成して実行する必要もあります。すべてのイベント ブロードキャストはキューに入れられたジョブを介して行われるため、ブロードキャストされるイベントによってアプリケーションの応答時間が重大な影響を受けることはありません。

<a name="reverb"></a>
<!-- ### Reverb -->
### Reverb

<!-- You may install Reverb using the Composer package manager: -->
Composer パッケージ マネージャーを使用して Reverb をインストールできます。

```sh
composer require laravel/reverb
```

<!-- Once the package is installed, you may run Reverb's installation command to publish the configuration, update your applications's broadcasting configuration, and add Reverb's required environment variables: -->
パッケージがインストールされたら、Reverb のインストール コマンドを実行して構成を公開し、アプリケーションのブロードキャスト構成を更新し、Reverb に必要な環境変数を追加できます。

```sh
php artisan reverb:install
```

<!-- You can find detailed Reverb installation and usage instructions in the [Reverb documentation](/docs/10.x/reverb). -->
Reverb のインストールと使用方法の詳細については、[Reverb documentation](/docs/10.x/reverb) を参照してください。

<a name="pusher-channels"></a>
<!-- ### Pusher Channels -->
### Pusher Channels

<!-- If you plan to broadcast your events using [Pusher Channels](https://pusher.com/channels), you should install the Pusher Channels PHP SDK using the Composer package manager: -->
[Pusher Channels](https://pusher.com/channels) を使用してイベントをブロードキャストする予定がある場合は、Composer パッケージ マネージャーを使用して Pusher Channels PHP SDK をインストールする必要があります。

```shell
composer require pusher/pusher-php-server
```

<!-- Next, you should configure your Pusher Channels credentials in the `config/broadcasting.php` configuration file. An example Pusher Channels configuration is already included in this file, allowing you to quickly specify your key, secret, and application ID. Typically, these values should be set via the `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, and `PUSHER_APP_ID` [environment variables](/docs/10.x/configuration#environment-configuration): -->
次に、`config/broadcasting.php` 構成ファイルでプッシャー チャネルの資格情報を構成する必要があります。このファイルにはプッシャー チャネル構成の例がすでに含まれており、キー、シークレット、アプリケーション ID をすばやく指定できます。通常、これらの値は、`PUSHER_APP_KEY`、`PUSHER_APP_SECRET`、および `PUSHER_APP_ID` [environment variables](/docs/10.x/configuration#environment-configuration) を介して設定する必要があります。

```ini
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

<!-- The `config/broadcasting.php` file's `pusher` configuration also allows you to specify additional `options` that are supported by Channels, such as the cluster. -->
`config/broadcasting.php` ファイルの `pusher` 構成では、クラスターなどのチャネルでサポートされる追加の `options` を指定することもできます。

<!-- Next, you will need to change your broadcast driver to `pusher` in your `.env` file: -->
次に、`.env` ファイル内のブロードキャスト ドライバを `pusher` に変更する必要があります。

```ini
BROADCAST_DRIVER=pusher
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
最後に、クライアント側でブロードキャスト イベントを受信する [Laravel Echo](#client-side-installation) をインストールして構成する準備が整いました。

<a name="pusher-compatible-open-source-alternatives"></a>
<!-- #### Open Source Pusher Alternatives -->
#### Open Source Pusher Alternatives

<!-- [soketi](https://docs.soketi.app/) provides a Pusher compatible WebSocket server for Laravel, allowing you to leverage the full power of Laravel broadcasting without a commercial WebSocket provider. For more information on installing and using open source packages for broadcasting, please consult our documentation on [open source alternatives](#open-source-alternatives). -->
[soketi](https://docs.soketi.app/) は、Laravel 用の Pusher 互換 WebSocket サーバーを提供し、商用 WebSocket プロバイダなしで Laravel ブロードキャストの能力を最大限に活用できるようにします。ブロードキャスト用のオープンソース パッケージのインストールと使用の詳細については、[open source alternatives](#open-source-alternatives) のドキュメントを参照してください。

<a name="ably"></a>
<!-- ### Ably -->
### Ably

> [!NOTE]
> 以下のドキュメントでは、Ably を「プッシャー互換性」モードで使用する方法について説明しています。ただし、Ably チームは、Ably が提供する独自の機能を活用できるブロードキャスタと Echo クライアントを推奨し、維持しています。 Ably が保守するドライバの使用の詳細については、[consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster) を参照してください。

<!-- If you plan to broadcast your events using [Ably](https://ably.com), you should install the Ably PHP SDK using the Composer package manager: -->
[Ably](https://ably.com) を使用してイベントをブロードキャストする予定がある場合は、Composer パッケージ マネージャーを使用して Ably PHP SDK をインストールする必要があります。

```shell
composer require ably/ably-php
```

<!-- Next, you should configure your Ably credentials in the `config/broadcasting.php` configuration file. An example Ably configuration is already included in this file, allowing you to quickly specify your key. Typically, this value should be set via the `ABLY_KEY` [environment variable](/docs/10.x/configuration#environment-configuration): -->
次に、`config/broadcasting.php` 構成ファイルで Ably 認証情報を構成する必要があります。このファイルには、Ably 構成の例がすでに含まれているため、キーをすばやく指定できます。通常、この値は `ABLY_KEY` [environment variable](/docs/10.x/configuration#environment-configuration) を介して設定する必要があります。

```ini
ABLY_KEY=your-ably-key
```

<!-- Next, you will need to change your broadcast driver to `ably` in your `.env` file: -->
次に、`.env` ファイル内のブロードキャスト ドライバを `ably` に変更する必要があります。

```ini
BROADCAST_DRIVER=ably
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
最後に、クライアント側でブロードキャスト イベントを受信する [Laravel Echo](#client-side-installation) をインストールして構成する準備が整いました。

<a name="open-source-alternatives"></a>
<!-- ### Open Source Alternatives -->
### Open Source Alternatives

<a name="open-source-alternatives-node"></a>
<!-- #### Node -->
#### Node

<!-- [Soketi](https://github.com/soketi/soketi) is a Node based, Pusher compatible WebSocket server for Laravel. Under the hood, Soketi utilizes µWebSockets.js for extreme scalability and speed. This package allows you to leverage the full power of Laravel broadcasting without a commercial WebSocket provider. For more information on installing and using this package, please consult its [official documentation](https://docs.soketi.app/). -->
[Soketi](https://github.com/soketi/soketi) は、Laravel 用のノードベースのプッシャー互換 WebSocket サーバーです。 Soketi は内部で µWebSockets.js を利用して、極めて高いスケーラビリティと速度を実現します。このパッケージを使用すると、商用 WebSocket プロバイダを使用せずに、Laravel ブロードキャストの機能を最大限に活用できます。このパッケージのインストールと使用の詳細については、[official documentation](https://docs.soketi.app/) を参照してください。

<a name="client-side-installation"></a>
<!-- ## Client Side Installation -->
## Client Side Installation

<a name="client-reverb"></a>
<!-- ### Reverb -->
### Reverb

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. You may install Echo via the NPM package manager. In this example, we will also install the `pusher-js` package since Reverb utilizes the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。 NPM パッケージ マネージャーを介して Echo をインストールできます。この例では、Reverb が WebSocket サブスクリプション、チャネル、メッセージにプッシャー プロトコルを利用するため、`pusher-js` パッケージもインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework. By default, an example Echo configuration is already included in this file - you simply need to uncomment it and update the `broadcaster` configuration option to `reverb`: -->
Echo をインストールすると、アプリケーションの JavaScript で新しい Echo インスタンスを作成できるようになります。これを行うのに最適な場所は、Laravel フレームワークに含まれる `resources/js/bootstrap.js` ファイルの下部です。デフォルトでは、Echo 設定の例はこのファイルにすでに含まれています。そのコメントを解除して、`broadcaster` 設定オプションを `reverb` に更新するだけです。

```js
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT,
    wssPort: import.meta.env.VITE_REVERB_PORT,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
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

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. You may install Echo via the NPM package manager. In this example, we will also install the `pusher-js` package since we will be using the Pusher Channels broadcaster: -->
[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。 NPM パッケージ マネージャーを介して Echo をインストールできます。この例では、Pusher Channels ブロードキャスタを使用するため、`pusher-js` パッケージもインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework. By default, an example Echo configuration is already included in this file - you simply need to uncomment it: -->
Echo をインストールすると、アプリケーションの JavaScript で新しい Echo インスタンスを作成できるようになります。これを行うのに最適な場所は、Laravel フレームワークに含まれる `resources/js/bootstrap.js` ファイルの下部です。デフォルトでは、Echo 設定の例がこのファイルにすでに含まれています。コメントを解除するだけです。

```js
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

<!-- Once you have uncommented and adjusted the Echo configuration according to your needs, you may compile your application's assets: -->
コメントを解除し、必要に応じて Echo 構成を調整したら、アプリケーションのアセットをコンパイルできます。

```shell
npm run build
```

> [!NOTE]
> アプリケーションの JavaScript アセットのコンパイルの詳細については、[Vite](/docs/10.x/vite) のドキュメントを参照してください。

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
    key: 'your-pusher-channels-key'
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

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. You may install Echo via the NPM package manager. In this example, we will also install the `pusher-js` package. -->
[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。 NPM パッケージ マネージャーを介して Echo をインストールできます。この例では、`pusher-js` パッケージもインストールします。

<!-- You may wonder why we would install the `pusher-js` JavaScript library even though we are using Ably to broadcast our events. Thankfully, Ably includes a Pusher compatibility mode which lets us use the Pusher protocol when listening for events in our client-side application: -->
イベントのブロードキャストに Ably を使用しているにもかかわらず、なぜ `pusher-js` JavaScript ライブラリをインストールするのか疑問に思われるかもしれません。ありがたいことに、Ably には、クライアント側アプリケーションでイベントをリッスンするときに Pusher プロトコルを使用できるようにする Pusher 互換モードが含まれています。

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- **Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.** -->
**続行する前に、Ably アプリケーション設定でプッシャー プロトコルのサポートを有効にする必要があります。 Ably アプリケーションの設定ダッシュボードの「プロトコル アダプター設定」部分でこの機能を有効にすることができます。**

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework. By default, an example Echo configuration is already included in this file; however, the default configuration in the `bootstrap.js` file is intended for Pusher. You may copy the configuration below to transition your configuration to Ably: -->
Echo をインストールすると、アプリケーションの JavaScript で新しい Echo インスタンスを作成できるようになります。これを行うのに最適な場所は、Laravel フレームワークに含まれる `resources/js/bootstrap.js` ファイルの下部です。デフォルトでは、Echo 設定の例がこのファイルにすでに含まれています。ただし、`bootstrap.js` ファイルのデフォルト設定はプッシャーを対象としています。以下の設定をコピーして、設定を Ably に移行できます。

```js
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

<!-- Note that our Ably Echo configuration references a `VITE_ABLY_PUBLIC_KEY` environment variable. This variable's value should be your Ably public key. Your public key is the portion of your Ably key that occurs before the `:` character. -->
Ably Echo 設定は `VITE_ABLY_PUBLIC_KEY` 環境変数を参照していることに注意してください。この変数の値は、Ably 公開キーである必要があります。公開キーは、Ably キーの `:` 文字の前にある部分です。

<!-- Once you have uncommented and adjusted the Echo configuration according to your needs, you may compile your application's assets: -->
コメントを解除し、必要に応じて Echo 構成を調整したら、アプリケーションのアセットをコンパイルできます。

```shell
npm run dev
```

> [!NOTE]
> アプリケーションの JavaScript アセットのコンパイルの詳細については、[Vite](/docs/10.x/vite) のドキュメントを参照してください。

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

<!-- Laravel's event broadcasting allows you to broadcast your server-side Laravel events to your client-side JavaScript application using a driver-based approach to WebSockets. Currently, Laravel ships with [Pusher Channels](https://pusher.com/channels) and [Ably](https://ably.com) drivers. The events may be easily consumed on the client-side using the [Laravel Echo](#client-side-installation) JavaScript package. -->
Laravel のイベント ブロードキャストを使用すると、WebSocket へのドライバベースのアプローチを使用して、サーバー側の Laravel イベントをクライアント側の JavaScript アプリケーションにブロードキャストできます。現在、Laravel には [Pusher Channels](https://pusher.com/channels) ドライバと [Ably](https://ably.com) ドライバが同梱されています。イベントは、[Laravel Echo](#client-side-installation) JavaScript パッケージを使用してクライアント側で簡単に使用できます。

<!-- Events are broadcast over "channels", which may be specified as public or private. Any visitor to your application may subscribe to a public channel without any authentication or authorization; however, in order to subscribe to a private channel, a user must be authenticated and authorized to listen on that channel. -->
イベントは、パブリックまたはプライベートとして指定できる「チャネル」を介してブロードキャストされます。アプリケーションへの訪問者は誰でも、認証や許可なしでパブリック チャネルに登録できます。ただし、プライベート チャネルに登録するには、ユーザーが認証され、そのチャネルでリッスンする権限が与えられている必要があります。

> [!NOTE]
> Pusher に代わるオープンソースの代替手段を検討したい場合は、[open source alternatives](#open-source-alternatives) をチェックしてください。

<a name="using-example-application"></a>
<!-- ### Using an Example Application -->
### Using an Example Application

<!-- Before diving into each component of event broadcasting, let's take a high level overview using an e-commerce store as an example. -->
イベント ブロードキャストの各コンポーネントに入る前に、電子商取引ストアを例として使用して概要を見てみましょう。

<!-- In our application, let's assume we have a page that allows users to view the shipping status for their orders. Let's also assume that an `OrderShipmentStatusUpdated` event is fired when a shipping status update is processed by the application: -->
このアプリケーションでは、ユーザーが注文の配送ステータスを表示できるページがあると仮定します。また、出荷ステータスの更新がアプリケーションによって処理されるときに、`OrderShipmentStatusUpdated` イベントが発生すると仮定します。

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
<!-- #### The `ShouldBroadcast` Interface -->
#### The `ShouldBroadcast` Interface

<!-- When a user is viewing one of their orders, we don't want them to have to refresh the page to view status updates. Instead, we want to broadcast the updates to the application as they are created. So, we need to mark the `OrderShipmentStatusUpdated` event with the `ShouldBroadcast` interface. This will instruct Laravel to broadcast the event when it is fired: -->
ユーザーが注文の 1 つを表示しているときに、ステータスの更新を表示するためにページを更新する必要がないようにしたいと考えています。代わりに、更新が作成されたときにアプリケーションに更新をブロードキャストしたいと考えています。したがって、`OrderShipmentStatusUpdated` イベントを `ShouldBroadcast` インターフェイスでマークする必要があります。これにより、Laravel がイベントの発生時にイベントをブロードキャストするように指示されます。

```
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

```
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

```
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

```
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

<!-- Next, all that remains is to listen for the event in our JavaScript application. We can do this using [Laravel Echo](#client-side-installation). First, we'll use the `private` method to subscribe to the private channel. Then, we may use the `listen` method to listen for the `OrderShipmentStatusUpdated` event. By default, all of the event's public properties will be included on the broadcast event: -->
次に残っているのは、JavaScript アプリケーションでイベントをリッスンすることだけです。これは、[Laravel Echo](#client-side-installation) を使用して行うことができます。まず、`private` メソッドを使用してプライベート チャネルに登録します。次に、`listen` メソッドを使用して、`OrderShipmentStatusUpdated` イベントをリッスンします。デフォルトでは、イベントのすべてのパブリック プロパティがブロードキャスト イベントに含まれます。

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
<!-- ## Defining Broadcast Events -->
## Defining Broadcast Events

<!-- To inform Laravel that a given event should be broadcast, you must implement the `Illuminate\Contracts\Broadcasting\ShouldBroadcast` interface on the event class. This interface is already imported into all event classes generated by the framework so you may easily add it to any of your events. -->
特定のイベントをブロードキャストする必要があることを Laravel に通知するには、イベント クラスに `Illuminate\Contracts\Broadcasting\ShouldBroadcast` インターフェイスを実装する必要があります。このインターフェイスは、フレームワークによって生成されたすべてのイベント クラスにすでにインポートされているため、任意のイベントに簡単に追加できます。

<!-- The `ShouldBroadcast` interface requires you to implement a single method: `broadcastOn`. The `broadcastOn` method should return a channel or array of channels that the event should broadcast on. The channels should be instances of `Channel`, `PrivateChannel`, or `PresenceChannel`. Instances of `Channel` represent public channels that any user may subscribe to, while `PrivateChannels` and `PresenceChannels` represent private channels that require [channel authorization](#authorizing-channels): -->
`ShouldBroadcast` インターフェイスでは、単一のメソッド `broadcastOn` を実装する必要があります。 `broadcastOn` メソッドは、イベントがブロードキャストされるチャネルまたはチャネルの配列を返す必要があります。チャネルは、`Channel`、`PrivateChannel`、または `PresenceChannel` のインスタンスである必要があります。 `Channel` のインスタンスは、任意のユーザーが購読できるパブリック チャネルを表し、`PrivateChannels` および `PresenceChannels` は、[channel authorization](#authorizing-channels) を必要とするプライベート チャネルを表します。

```
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

<!-- After implementing the `ShouldBroadcast` interface, you only need to [fire the event](/docs/10.x/events) as you normally would. Once the event has been fired, a [queued job](/docs/10.x/queues) will automatically broadcast the event using your specified broadcast driver. -->
`ShouldBroadcast` インターフェイスを実装した後は、通常どおり [fire the event](/docs/10.x/events) を実行するだけです。イベントが発生すると、[queued job](/docs/10.x/queues) は指定したブロードキャスト ドライバを使用してイベントを自動的にブロードキャストします。

<a name="broadcast-name"></a>
<!-- ### Broadcast Name -->
### Broadcast Name

<!-- By default, Laravel will broadcast the event using the event's class name. However, you may customize the broadcast name by defining a `broadcastAs` method on the event: -->
デフォルトでは、Laravel はイベントのクラス名を使用してイベントをブロードキャストします。ただし、イベントで `broadcastAs` メソッドを定義することで、ブロードキャスト名をカスタマイズできます。

```
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

```
.listen('.server.created', function (e) {
    ....
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

```
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

<!-- By default, each broadcast event is placed on the default queue for the default queue connection specified in your `queue.php` configuration file. You may customize the queue connection and name used by the broadcaster by defining `connection` and `queue` properties on your event class: -->
デフォルトでは、各ブロードキャスト イベントは、`queue.php` 構成ファイルで指定されたデフォルト キュー接続のデフォルト キューに配置されます。イベント クラスで `connection` プロパティと `queue` プロパティを定義することで、ブロードキャスタが使用するキュー接続と名前をカスタマイズできます。

```
/**
 * The name of the queue connection to use when broadcasting the event.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * The name of the queue on which to place the broadcasting job.
 *
 * @var string
 */
public $queue = 'default';
```

<!-- Alternatively, you may customize the queue name by defining a `broadcastQueue` method on your event: -->
あるいは、イベントで `broadcastQueue` メソッドを定義してキュー名をカスタマイズすることもできます。

```
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

```
<?php

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

```
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

```
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
> これらの問題の回避方法の詳細については、[queued jobs and database transactions](/docs/10.x/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="authorizing-channels"></a>
<!-- ## Authorizing Channels -->
## Authorizing Channels

<!-- Private channels require you to authorize that the currently authenticated user can actually listen on the channel. This is accomplished by making an HTTP request to your Laravel application with the channel name and allowing your application to determine if the user can listen on that channel. When using [Laravel Echo](#client-side-installation), the HTTP request to authorize subscriptions to private channels will be made automatically; however, you do need to define the proper routes to respond to these requests. -->
プライベート チャネルでは、現在認証されているユーザーが実際にチャネルをリッスンできることを承認する必要があります。これは、チャンネル名を使用して Laravel アプリケーションに HTTP リクエストを送信し、ユーザーがそのチャンネルでリッスンできるかどうかをアプリケーションが判断できるようにすることで実現されます。 [Laravel Echo](#client-side-installation) を使用すると、プライベート チャネルへのサブスクリプションを承認する HTTP リクエストが自動的に作成されます。ただし、これらのリクエストに応答するために適切なルートを定義する必要があります。

<a name="defining-authorization-routes"></a>
<!-- ### Defining Authorization Routes -->
### Defining Authorization Routes

<!-- Thankfully, Laravel makes it easy to define the routes to respond to channel authorization requests. In the `App\Providers\BroadcastServiceProvider` included with your Laravel application, you will see a call to the `Broadcast::routes` method. This method will register the `/broadcasting/auth` route to handle authorization requests: -->
ありがたいことに、Laravel では、チャネル承認リクエストに応答するルートを簡単に定義できます。 Laravel アプリケーションに含まれる `App\Providers\BroadcastServiceProvider` には、`Broadcast::routes` メソッドの呼び出しが表示されます。このメソッドは、認可リクエストを処理するために `/broadcasting/auth` ルートを登録します。

```
Broadcast::routes();
```

<!-- The `Broadcast::routes` method will automatically place its routes within the `web` middleware group; however, you may pass an array of route attributes to the method if you would like to customize the assigned attributes: -->
`Broadcast::routes` メソッドは、そのルートを `web` ミドルウェア グループ内に自動的に配置します。ただし、割り当てられた属性をカスタマイズしたい場合は、ルート属性の配列をメソッドに渡すことができます。

```
Broadcast::routes($attributes);
```

<a name="customizing-the-authorization-endpoint"></a>
<!-- #### Customizing the Authorization Endpoint -->
#### Customizing the Authorization Endpoint

<!-- By default, Echo will use the `/broadcasting/auth` endpoint to authorize channel access. However, you may specify your own authorization endpoint by passing the `authEndpoint` configuration option to your Echo instance: -->
デフォルトでは、Echo は `/broadcasting/auth` エンドポイントを使用してチャネル アクセスを認可します。ただし、`authEndpoint` 構成オプションを Echo インスタンスに渡すことで、独自の認可エンドポイントを指定できます。

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
<!-- #### Customizing the Authorization Request -->
#### Customizing the Authorization Request

<!-- You can customize how Laravel Echo performs authorization requests by providing a custom authorizer when initializing Echo: -->
Echoの初期化時にカスタム承認者を提供することで、Laravel Echoが承認リクエストを実行する方法をカスタマイズできます。

```js
window.Echo = new Echo({
    // ...
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(null, response.data);
                })
                .catch(error => {
                    callback(error);
                });
            }
        };
    },
})
```

<a name="defining-authorization-callbacks"></a>
<!-- ### Defining Authorization Callbacks -->
### Defining Authorization Callbacks

<!-- Next, we need to define the logic that will actually determine if the currently authenticated user can listen to a given channel. This is done in the `routes/channels.php` file that is included with your application. In this file, you may use the `Broadcast::channel` method to register channel authorization callbacks: -->
次に、現在認証されているユーザーが特定のチャンネルを聞くことができるかどうかを実際に判断するロジックを定義する必要があります。これは、アプリケーションに含まれる `routes/channels.php` ファイルで行われます。このファイルでは、`Broadcast::channel` メソッドを使用してチャネル承認コールバックを登録できます。

```
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

<!-- Just like HTTP routes, channel routes may also take advantage of implicit and explicit [route model binding](/docs/10.x/routing#route-model-binding). For example, instead of receiving a string or numeric order ID, you may request an actual `Order` model instance: -->
HTTP ルートと同様に、チャネル ルートも暗黙的および明示的な [route model binding](/docs/10.x/routing#route-model-binding) を利用できます。たとえば、文字列または数値の注文 ID を受け取る代わりに、実際の `Order` モデル インスタンスをリクエストできます。

```
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP ルート モデル バインディングとは異なり、チャネル モデル バインディングは自動 [implicit model binding scoping](/docs/10.x/routing#implicit-model-binding-scoping) をサポートしません。ただし、ほとんどのチャネルは単一モデルの一意の主キーに基づいてスコープを設定できるため、これが問題になることはほとんどありません。

<a name="authorization-callback-authentication"></a>
<!-- #### Authorization Callback Authentication -->
#### Authorization Callback Authentication

<!-- Private and presence broadcast channels authenticate the current user via your application's default authentication guard. If the user is not authenticated, channel authorization is automatically denied and the authorization callback is never executed. However, you may assign multiple, custom guards that should authenticate the incoming request if necessary: -->
プライベート ブロードキャスト チャネルとプレゼンス ブロードキャスト チャネルは、アプリケーションのデフォルトの認証ガードを介して現在のユーザーを認証します。ユーザーが認証されていない場合、チャネル承認は自動的に拒否され、承認コールバックは実行されません。ただし、必要に応じて、受信リクエストを認証する複数のカスタム ガードを割り当てることができます。

```
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

```
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

<!-- Finally, you may place the authorization logic for your channel in the channel class' `join` method. This `join` method will house the same logic you would have typically placed in your channel authorization closure. You may also take advantage of channel model binding: -->
最後に、チャネル クラスの `join` メソッドにチャネルの承認ロジックを配置できます。この `join` メソッドには、通常チャネル承認クロージャに配置するのと同じロジックが格納されます。チャネル モデル バインディングを利用することもできます。

```
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct()
    {
        // ...
    }

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
> Laravel の他の多くのクラスと同様に、チャネル クラスは [service container](/docs/10.x/container) によって自動的に解決されます。したがって、コンストラクターでチャネルに必要な依存関係をタイプヒントで指定できます。

<a name="broadcasting-events"></a>
<!-- ## Broadcasting Events -->
## Broadcasting Events

<!-- Once you have defined an event and marked it with the `ShouldBroadcast` interface, you only need to fire the event using the event's dispatch method. The event dispatcher will notice that the event is marked with the `ShouldBroadcast` interface and will queue the event for broadcasting: -->
イベントを定義し、それを `ShouldBroadcast` インターフェイスでマークしたら、あとはイベントのディスパッチ メソッドを使用してイベントを起動するだけです。イベント ディスパッチャは、イベントが `ShouldBroadcast` インターフェイスでマークされていることを認識し、ブロードキャスト用にイベントをキューに入れます。

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
<!-- ### Only to Others -->
### Only to Others

<!-- When building an application that utilizes event broadcasting, you may occasionally need to broadcast an event to all subscribers to a given channel except for the current user. You may accomplish this using the `broadcast` helper and the `toOthers` method: -->
イベント ブロードキャストを利用するアプリケーションを構築する場合、現在のユーザーを除く特定のチャネルのすべての加入者にイベントをブロードキャストすることが必要になる場合があります。これは、`broadcast` ヘルパと `toOthers` メソッドを使用して実現できます。

```
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

<!-- When you initialize a Laravel Echo instance, a socket ID is assigned to the connection. If you are using a global [Axios](https://github.com/mzabriskie/axios) instance to make HTTP requests from your JavaScript application, the socket ID will automatically be attached to every outgoing request as an `X-Socket-ID` header. Then, when you call the `toOthers` method, Laravel will extract the socket ID from the header and instruct the broadcaster to not broadcast to any connections with that socket ID. -->
Laravel Echo インスタンスを初期化すると、接続にソケット ID が割り当てられます。グローバル [Axios](https://github.com/mzabriskie/axios) インスタンスを使用して JavaScript アプリケーションから HTTP リクエストを作成している場合、ソケット ID はすべての発信リクエストに `X-Socket-ID` ヘッダーとして自動的に付加されます。次に、`toOthers` メソッドを呼び出すと、Laravel はヘッダーからソケット ID を抽出し、そのソケット ID を持つ接続にブロードキャストしないようにブロードキャスタに指示します。

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

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

<!-- Alternatively, you may specify the event's broadcast connection by calling the `broadcastVia` method within the event's constructor. However, before doing so, you should ensure that the event class uses the `InteractsWithBroadcasting` trait: -->
あるいは、イベントのコンストラクター内で `broadcastVia` メソッドを呼び出して、イベントのブロードキャスト接続を指定することもできます。ただし、これを行う前に、イベント クラスが `InteractsWithBroadcasting` 特性を使用していることを確認する必要があります。

```
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
    .stopListening('OrderShipmentStatusUpdated')
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

```
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

```
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

```
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

<!-- It is common to broadcast events when your application's [Eloquent models](/docs/10.x/eloquent) are created, updated, or deleted. Of course, this can easily be accomplished by manually [defining custom events for Eloquent model state changes](/docs/10.x/eloquent#events) and marking those events with the `ShouldBroadcast` interface. -->
アプリケーションの [Eloquent models](/docs/10.x/eloquent) が作成、更新、または削除されたときにイベントをブロードキャストするのが一般的です。もちろん、これは手動で [defining custom events for Eloquent model state changes](/docs/10.x/eloquent#events) を実行し、それらのイベントを `ShouldBroadcast` インターフェイスでマークすることで簡単に実現できます。

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
$user->broadcastChannel()
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
    "socket": "someSocketId",
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
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
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

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

<!-- To listen for client events, you may use the `listenForWhisper` method: -->
クライアント イベントをリッスンするには、`listenForWhisper` メソッドを使用できます。

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<!-- By pairing event broadcasting with [notifications](/docs/10.x/notifications), your JavaScript application may receive new notifications as they occur without needing to refresh the page. Before getting started, be sure to read over the documentation on using [the broadcast notification channel](/docs/10.x/notifications#broadcast-notifications). -->
イベント ブロードキャストと [notifications](/docs/10.x/notifications) を組み合わせることにより、JavaScript アプリケーションは、ページを更新しなくても、新しい通知が発生したときに受信できるようになります。始める前に、[the broadcast notification channel](/docs/10.x/notifications#broadcast-notifications) の使用に関するドキュメントを必ずお読みください。

<!-- Once you have configured a notification to use the broadcast channel, you may listen for the broadcast events using Echo's `notification` method. Remember, the channel name should match the class name of the entity receiving the notifications: -->
ブロードキャスト チャネルを使用するように通知を構成したら、Echo の `notification` メソッドを使用してブロードキャスト イベントをリッスンできます。チャネル名は、通知を受信するエンティティのクラス名と一致する必要があることに注意してください。

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<!-- In this example, all notifications sent to `App\Models\User` instances via the `broadcast` channel would be received by the callback. A channel authorization callback for the `App.Models.User.{id}` channel is included in the default `BroadcastServiceProvider` that ships with the Laravel framework. -->
この例では、`broadcast` チャネル経由で `App\Models\User` インスタンスに送信されたすべての通知がコールバックによって受信されます。 `App.Models.User.{id}` チャネルのチャネル認可コールバックは、Laravel フレームワークに付属するデフォルトの `BroadcastServiceProvider` に含まれています。

