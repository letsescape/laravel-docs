# 放送 (Broadcasting)

- [Introduction](#introduction)
- [サーバー側のインストール](#server-side-installation)
    - [Configuration](#configuration)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [オープンソースの代替案](#open-source-alternatives)
- [クライアント側のインストール](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [コンセプトの概要](#concept-overview)
    - [サンプルアプリケーションの使用](#using-example-application)
- [ブロードキャスト イベントの定義](#defining-broadcast-events)
    - [ブロードキャスト名](#broadcast-name)
    - [ブロードキャストデータ](#broadcast-data)
    - [ブロードキャストキュー](#broadcast-queue)
    - [放送条件](#broadcast-conditions)
    - [ブロードキャストとデータベーストランザクション](#broadcasting-and-database-transactions)
- [チャネルの承認](#authorizing-channels)
    - [認可ルートの定義](#defining-authorization-routes)
    - [認可コールバックの定義](#defining-authorization-callbacks)
    - [チャネルクラスの定義](#defining-channel-classes)
- [イベントの放送](#broadcasting-events)
    - [他人だけに](#only-to-others)
    - [接続のカスタマイズ](#customizing-the-connection)
- [ブロードキャストを受信する](#receiving-broadcasts)
    - [イベントをリッスンする](#listening-for-events)
    - [チャンネルを離れる](#leaving-a-channel)
    - [Namespaces](#namespaces)
- [プレゼンスチャンネル](#presence-channels)
    - [プレゼンスチャネルの承認](#authorizing-presence-channels)
    - [プレゼンスチャンネルへの参加](#joining-presence-channels)
    - [プレゼンスチャネルへのブロードキャスト](#broadcasting-to-presence-channels)
- [モデル放送](#model-broadcasting)
    - [モデル放送規約](#model-broadcasting-conventions)
    - [モデルブロードキャストを聞く](#listening-for-model-broadcasts)
- [クライアントイベント](#client-events)
- [Notifications](#notifications)

<a name="introduction"></a>
## 導入 (Introduction)

最新の Web アプリケーションの多くでは、リアルタイムのライブ更新ユーザー インターフェイスを実装するために WebSocket が使用されています。サーバー上で一部のデータが更新されると、通常、メッセージが WebSocket 接続経由で送信され、クライアントによって処理されます。 WebSocket は、UI に反映する必要があるデータ変更をアプリケーションのサーバーに継続的にポーリングするより効率的な代替手段を提供します。

たとえば、アプリケーションがユーザーのデータを CSV ファイルにエクスポートし、電子メールで送信できると想像してください。ただし、この CSV ファイルの作成には数分かかるため、[キューに入れられたジョブ](/docs/{{version}}/queues) 内で CSV を作成してメールで送信することを選択します。 CSV が作成され、ユーザーにメールで送信されたら、イベント ブロードキャストを使用して、アプリケーションの JavaScript が受信する `App\Events\UserDataExported` イベントを送出できます。イベントを受信すると、ページを更新しなくても、CSV が電子メールで送信されたことを示すメッセージをユーザーに表示できます。

この種の機能の構築を支援するために、Laravel では、WebSocket 接続を介してサーバー側 Laravel [events](/docs/{{version}}/events) を簡単に「ブロードキャスト」できるようにしています。 Laravel イベントをブロードキャストすると、サーバー側の Laravel アプリケーションとクライアント側の JavaScript アプリケーションの間で同じイベント名とデータを共有できます。

ブロードキャストの背後にある中心的な概念は単純です。クライアントはフロントエンドの名前付きチャネルに接続し、Laravel アプリケーションはバックエンドのこれらのチャネルにイベントをブロードキャストします。これらのイベントには、フロントエンドで利用できるようにしたい追加データを含めることができます。

<a name="supported-drivers"></a>
#### サポートされているドライバ

デフォルトでは、Laravel には、[Laravel Reverb](https://reverb.laravel.com)、[Pusher Channels](https://pusher.com/channels)、および [Ably](https://ably.com) から選択できる 3 つのサーバー側ブロードキャスト ドライバが含まれています。

> [!NOTE]  
> イベントブロードキャストに入る前に、[イベントとリスナ](/docs/{{version}}/events) にある Laravel のドキュメントを必ず読んでください。

<a name="server-side-installation"></a>
## サーバー側のインストール (Server Side Installation)

Laravel のイベントブロードキャストの使用を開始するには、Laravel アプリケーション内でいくつかの設定を行い、いくつかのパッケージをインストールする必要があります。

イベントのブロードキャストは、Laravel イベントをブロードキャストするサーバー側ブロードキャスト ドライバによって実現され、Laravel Echo (JavaScript ライブラリ) がブラウザー クライアント内でイベントを受信できるようになります。心配しないでください。インストール プロセスの各部分を段階的に説明します。

<a name="configuration"></a>
### 構成

アプリケーションのイベント ブロードキャスト設定はすべて、`config/broadcasting.php` 設定ファイルに保存されます。 Laravel は、すぐに使用できるいくつかのブロードキャスト ドライバ (ローカル開発およびデバッグ用の [Pusher Channels](https://pusher.com/channels)、[Redis](/docs/{{version}}/redis)、および `log` ドライバ) をサポートしています。さらに、テスト中にブロードキャストを完全に無効にすることができる `null` ドライバが含まれています。これらの各ドライバの構成例は、`config/broadcasting.php` 構成ファイルに含まれています。

<a name="broadcast-service-provider"></a>
#### ブロードキャストサービスプロバイダ

イベントをブロードキャストする前に、まず `App\Providers\BroadcastServiceProvider` を登録する必要があります。新しい Laravel アプリケーションでは、`config/app.php` 構成ファイルの `providers` 配列でこのプロバイダのコメントを解除するだけで済みます。この `BroadcastServiceProvider` には、ブロードキャスト認証ルートとコールバックを登録するために必要なコードが含まれています。

<a name="queue-configuration"></a>
#### キュー構成

[キューワーカー](/docs/{{version}}/queues) を構成して実行する必要もあります。すべてのイベント ブロードキャストはキューに入れられたジョブを介して行われるため、ブロードキャストされるイベントによってアプリケーションの応答時間が重大な影響を受けることはありません。

<a name="reverb"></a>
### Reverb

Composer パッケージ マネージャーを使用して Reverb をインストールできます。

```sh
composer require laravel/reverb
```

パッケージがインストールされたら、Reverb のインストール コマンドを実行して構成を公開し、アプリケーションのブロードキャスト構成を更新し、Reverb に必要な環境変数を追加できます。

```sh
php artisan reverb:install
```

Reverb のインストールと使用方法の詳細については、[Reverb のドキュメント](/docs/{{version}}/reverb) を参照してください。

<a name="pusher-channels"></a>
### Pusher Channels

[Pusher Channels](https://pusher.com/channels) を使用してイベントをブロードキャストする予定がある場合は、Composer パッケージ マネージャーを使用して Pusher Channels PHP SDK をインストールする必要があります。

```shell
composer require pusher/pusher-php-server
```

次に、`config/broadcasting.php` 構成ファイルでプッシャー チャネルの資格情報を構成する必要があります。このファイルにはプッシャー チャネル構成の例がすでに含まれており、キー、シークレット、アプリケーション ID をすばやく指定できます。通常、これらの値は、`PUSHER_APP_KEY`、`PUSHER_APP_SECRET`、および `PUSHER_APP_ID` [環境変数](/docs/{{version}}/configuration#environment-configuration) を介して設定する必要があります。

```ini
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

`config/broadcasting.php` ファイルの `pusher` 構成では、クラスターなどのチャネルでサポートされる追加の `options` を指定することもできます。

次に、`.env` ファイル内のブロードキャスト ドライバを `pusher` に変更する必要があります。

```ini
BROADCAST_DRIVER=pusher
```

最後に、クライアント側でブロードキャスト イベントを受信する [Laravel Echo](#client-side-installation) をインストールして構成する準備が整いました。

<a name="pusher-compatible-open-source-alternatives"></a>
#### オープンソースのプッシャー代替手段

[soketi](https://docs.soketi.app/) は、Laravel 用の Pusher 互換 WebSocket サーバーを提供し、商用 WebSocket プロバイダなしで Laravel ブロードキャストの能力を最大限に活用できるようにします。ブロードキャスト用のオープンソース パッケージのインストールと使用の詳細については、[オープンソースの代替品](#open-source-alternatives) のドキュメントを参照してください。

<a name="ably"></a>
### アブレイ

> [!NOTE]  
> 以下のドキュメントでは、Ably を「プッシャー互換性」モードで使用する方法について説明しています。ただし、Ably チームは、Ably が提供する独自の機能を活用できるブロードキャスタと Echo クライアントを推奨し、維持しています。 Ably が保守するドライバの使用の詳細については、[Ably の Laravel ブロードキャスタのドキュメントを参照してください。](https://github.com/ably/laravel-broadcaster) を参照してください。

[Ably](https://ably.com) を使用してイベントをブロードキャストする予定がある場合は、Composer パッケージ マネージャーを使用して Ably PHP SDK をインストールする必要があります。

```shell
composer require ably/ably-php
```

次に、`config/broadcasting.php` 構成ファイルで Ably 認証情報を構成する必要があります。このファイルには、Ably 構成の例がすでに含まれているため、キーをすばやく指定できます。通常、この値は `ABLY_KEY` [環境変数](/docs/{{version}}/configuration#environment-configuration) を介して設定する必要があります。

```ini
ABLY_KEY=your-ably-key
```

次に、`.env` ファイル内のブロードキャスト ドライバを `ably` に変更する必要があります。

```ini
BROADCAST_DRIVER=ably
```

最後に、クライアント側でブロードキャスト イベントを受信する [Laravel Echo](#client-side-installation) をインストールして構成する準備が整いました。

<a name="open-source-alternatives"></a>
### オープンソースの代替案

<a name="open-source-alternatives-node"></a>
#### ノード

[Soketi](https://github.com/soketi/soketi) は、Laravel 用のノードベースのプッシャー互換 WebSocket サーバーです。 Soketi は内部で µWebSockets.js を利用して、極めて高いスケーラビリティと速度を実現します。このパッケージを使用すると、商用 WebSocket プロバイダを使用せずに、Laravel ブロードキャストの機能を最大限に活用できます。このパッケージのインストールと使用の詳細については、[公式ドキュメント](https://docs.soketi.app/) を参照してください。

<a name="client-side-installation"></a>
## クライアント側のインストール (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。 NPM パッケージ マネージャーを介して Echo をインストールできます。この例では、Reverb が WebSocket サブスクリプション、チャネル、メッセージにプッシャー プロトコルを利用するため、`pusher-js` パッケージもインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

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

次に、アプリケーションのアセットをコンパイルする必要があります。

```shell
npm run build
```

> [!WARNING]  
> Laravel Echo `reverb` ブロードキャスタには、laravel-echo v1.16.0+ が必要です。

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。 NPM パッケージ マネージャーを介して Echo をインストールできます。この例では、Pusher Channels ブロードキャスタを使用するため、`pusher-js` パッケージもインストールします。

```shell
npm install --save-dev laravel-echo pusher-js
```

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

コメントを解除し、必要に応じて Echo 構成を調整したら、アプリケーションのアセットをコンパイルできます。

```shell
npm run build
```

> [!NOTE]  
> アプリケーションの JavaScript アセットのコンパイルの詳細については、[Vite](/docs/{{version}}/vite) のドキュメントを参照してください。

<a name="using-an-existing-client-instance"></a>
#### 既存のクライアント インスタンスの使用

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
### アブレイ

> [!NOTE]  
> 以下のドキュメントでは、Ably を「プッシャー互換性」モードで使用する方法について説明しています。ただし、Ably チームは、Ably が提供する独自の機能を活用できるブロードキャスタと Echo クライアントを推奨し、維持しています。 Ably が保守するドライバの使用の詳細については、[Ably の Laravel ブロードキャスタのドキュメントを参照してください。](https://github.com/ably/laravel-broadcaster) を参照してください。

[Laravel Echo](https://github.com/laravel/echo) は、チャンネルのサブスクライブや、サーバー側のブロードキャスト ドライバによってブロードキャストされるイベントのリッスンを簡単に行うことができる JavaScript ライブラリです。 NPM パッケージ マネージャーを介して Echo をインストールできます。この例では、`pusher-js` パッケージもインストールします。

イベントのブロードキャストに Ably を使用しているにもかかわらず、なぜ `pusher-js` JavaScript ライブラリをインストールするのか疑問に思われるかもしれません。ありがたいことに、Ably には、クライアント側アプリケーションでイベントをリッスンするときに Pusher プロトコルを使用できるようにする Pusher 互換モードが含まれています。

```shell
npm install --save-dev laravel-echo pusher-js
```

**続行する前に、Ably アプリケーション設定でプッシャー プロトコルのサポートを有効にする必要があります。 Ably アプリケーションの設定ダッシュボードの「プロトコル アダプター設定」部分でこの機能を有効にすることができます。**

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

Ably Echo 設定は `VITE_ABLY_PUBLIC_KEY` 環境変数を参照していることに注意してください。この変数の値は、Ably 公開キーである必要があります。公開キーは、Ably キーの `:` 文字の前にある部分です。

コメントを解除し、必要に応じて Echo 構成を調整したら、アプリケーションのアセットをコンパイルできます。

```shell
npm run dev
```

> [!NOTE]  
> アプリケーションの JavaScript アセットのコンパイルの詳細については、[Vite](/docs/{{version}}/vite) のドキュメントを参照してください。

<a name="concept-overview"></a>
## コンセプトの概要 (Concept Overview)

Laravel のイベント ブロードキャストを使用すると、WebSocket へのドライバベースのアプローチを使用して、サーバー側の Laravel イベントをクライアント側の JavaScript アプリケーションにブロードキャストできます。現在、Laravel には [Pusher Channels](https://pusher.com/channels) ドライバと [Ably](https://ably.com) ドライバが同梱されています。イベントは、[Laravel Echo](#client-side-installation) JavaScript パッケージを使用してクライアント側で簡単に使用できます。

イベントは、パブリックまたはプライベートとして指定できる「チャネル」を介してブロードキャストされます。アプリケーションへの訪問者は誰でも、認証や許可なしでパブリック チャネルに登録できます。ただし、プライベート チャネルに登録するには、ユーザーが認証され、そのチャネルでリッスンする権限が与えられている必要があります。

> [!NOTE]  
> Pusher に代わるオープンソースの代替手段を検討したい場合は、[オープンソースの代替品](#open-source-alternatives) をチェックしてください。

<a name="using-example-application"></a>
### サンプルアプリケーションの使用

イベント ブロードキャストの各コンポーネントに入る前に、電子商取引ストアを例として使用して概要を見てみましょう。

このアプリケーションでは、ユーザーが注文の配送ステータスを表示できるページがあると仮定します。また、出荷ステータスの更新がアプリケーションによって処理されるときに、`OrderShipmentStatusUpdated` イベントが発生すると仮定します。

    use App\Events\OrderShipmentStatusUpdated;

    OrderShipmentStatusUpdated::dispatch($order);

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` インターフェイス

ユーザーが注文の 1 つを表示しているときに、ステータスの更新を表示するためにページを更新する必要がないようにしたいと考えています。代わりに、更新が作成されたときにアプリケーションに更新をブロードキャストしたいと考えています。したがって、`OrderShipmentStatusUpdated` イベントを `ShouldBroadcast` インターフェイスでマークする必要があります。これにより、Laravel がイベントの発生時にイベントをブロードキャストするように指示されます。

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

`ShouldBroadcast` インターフェイスでは、イベントで `broadcastOn` メソッドを定義する必要があります。このメソッドは、イベントがブロードキャストされるチャネルを返す役割を果たします。このメソッドの空のスタブは生成されたイベント クラスですでに定義されているため、その詳細を入力するだけで済みます。注文の作成者のみがステータス更新を表示できるようにしたいため、注文に関連付けられたプライベート チャネルでイベントをブロードキャストします。

    use Illuminate\Broadcasting\Channel;
    use Illuminate\Broadcasting\PrivateChannel;

    /**
     * Get the channel the event should broadcast on.
     */
    public function broadcastOn(): Channel
    {
        return new PrivateChannel('orders.'.$this->order->id);
    }

イベントを複数のチャンネルでブロードキャストしたい場合は、代わりに `array` を返すことができます。

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

<a name="example-application-authorizing-channels"></a>
#### チャネルの承認

ユーザーはプライベート チャネルでリッスンすることを許可されている必要があることに注意してください。アプリケーションの `routes/channels.php` ファイルでチャネル認証ルールを定義できます。この例では、プライベート `orders.1` チャネルでリッスンしようとしているユーザーが実際に注文の作成者であることを確認する必要があります。

    use App\Models\Order;
    use App\Models\User;

    Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
        return $user->id === Order::findOrNew($orderId)->user_id;
    });

`channel` メソッドは、チャネルの名前と、ユーザーがチャネルでリッスンする権限があるかどうかを示す `true` または `false` を返すコールバックの 2 つの引数を受け入れます。

すべての認可コールバックは、現在認証されているユーザーを最初の引数として受け取り、追加のワイルドカード パラメーターを後続の引数として受け取ります。この例では、`{orderId}` プレースホルダーを使用して、チャネル名の「ID」部分がワイルドカードであることを示しています。

<a name="listening-for-event-broadcasts"></a>
#### イベントブロードキャストのリスニング

次に残っているのは、JavaScript アプリケーションでイベントをリッスンすることだけです。これは、[Laravel Echo](#client-side-installation) を使用して行うことができます。まず、`private` メソッドを使用してプライベート チャネルに登録します。次に、`listen` メソッドを使用して、`OrderShipmentStatusUpdated` イベントをリッスンします。デフォルトでは、イベントのすべてのパブリック プロパティがブロードキャスト イベントに含まれます。

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>
## ブロードキャスト イベントの定義 (Defining Broadcast Events)

特定のイベントをブロードキャストする必要があることを Laravel に通知するには、イベント クラスに `Illuminate\Contracts\Broadcasting\ShouldBroadcast` インターフェイスを実装する必要があります。このインターフェイスは、フレームワークによって生成されたすべてのイベント クラスにすでにインポートされているため、任意のイベントに簡単に追加できます。

`ShouldBroadcast` インターフェイスでは、単一のメソッド `broadcastOn` を実装する必要があります。 `broadcastOn` メソッドは、イベントがブロードキャストされるチャネルまたはチャネルの配列を返す必要があります。チャネルは、`Channel`、`PrivateChannel`、または `PresenceChannel` のインスタンスである必要があります。 `Channel` のインスタンスは、任意のユーザーが購読できるパブリック チャネルを表し、`PrivateChannels` および `PresenceChannels` は、[チャネル認証](#authorizing-channels) を必要とするプライベート チャネルを表します。

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

`ShouldBroadcast` インターフェイスを実装した後は、通常どおり [イベントを起動する](/docs/{{version}}/events) を実行するだけです。イベントが発生すると、[キューに入れられたジョブ](/docs/{{version}}/queues) は指定したブロードキャスト ドライバを使用してイベントを自動的にブロードキャストします。

<a name="broadcast-name"></a>
### ブロードキャスト名

デフォルトでは、Laravel はイベントのクラス名を使用してイベントをブロードキャストします。ただし、イベントで `broadcastAs` メソッドを定義することで、ブロードキャスト名をカスタマイズできます。

    /**
     * The event's broadcast name.
     */
    public function broadcastAs(): string
    {
        return 'server.created';
    }

`broadcastAs` メソッドを使用してブロードキャスト名をカスタマイズする場合は、先頭に `.` 文字を使用してリスナを登録する必要があります。これにより、アプリケーションの名前空間をイベントの前に付加しないように Echo に指示されます。

    .listen('.server.created', function (e) {
        ....
    });

<a name="broadcast-data"></a>
### ブロードキャストデータ

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

ただし、ブロードキャスト ペイロードをより細かく制御したい場合は、イベントに `broadcastWith` メソッドを追加できます。このメソッドは、イベント ペイロードとしてブロードキャストするデータの配列を返す必要があります。

    /**
     * Get the data to broadcast.
     *
     * @return array<string, mixed>
     */
    public function broadcastWith(): array
    {
        return ['id' => $this->user->id];
    }

<a name="broadcast-queue"></a>
### ブロードキャストキュー

デフォルトでは、各ブロードキャスト イベントは、`queue.php` 構成ファイルで指定されたデフォルト キュー接続のデフォルト キューに配置されます。イベント クラスで `connection` プロパティと `queue` プロパティを定義することで、ブロードキャスタが使用するキュー接続と名前をカスタマイズできます。

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

あるいは、イベントで `broadcastQueue` メソッドを定義してキュー名をカスタマイズすることもできます。

    /**
     * The name of the queue on which to place the broadcasting job.
     */
    public function broadcastQueue(): string
    {
        return 'default';
    }

デフォルトのキュードライバの代わりに `sync` キューを使用してイベントをブロードキャストする場合は、`ShouldBroadcast` の代わりに `ShouldBroadcastNow` インターフェイスを実装できます。

    <?php

    use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

    class OrderShipmentStatusUpdated implements ShouldBroadcastNow
    {
        // ...
    }

<a name="broadcast-conditions"></a>
### 放送条件

特定の条件が true の場合にのみイベントをブロードキャストしたい場合があります。これらの条件は、イベント クラスに `broadcastWhen` メソッドを追加することで定義できます。

    /**
     * Determine if this event should broadcast.
     */
    public function broadcastWhen(): bool
    {
        return $this->order->value > 100;
    }

<a name="broadcasting-and-database-transactions"></a>
#### ブロードキャストとデータベーストランザクション

ブロードキャスト イベントがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される場合があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。イベントがこれらのモデルに依存している場合、イベントをブロードキャストするジョブの処理時に予期しないエラーが発生する可能性があります。

キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、イベント クラスに `ShouldDispatchAfterCommit` インターフェイスを実装することで、開いているすべてのデータベース トランザクションがコミットされた後に特定のブロードキャスト イベントをディスパッチする必要があることを示すことができます。

    <?php

    namespace App\Events;

    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
    use Illuminate\Queue\SerializesModels;

    class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
    {
        use SerializesModels;
    }

> [!NOTE]  
> これらの問題の回避方法の詳細については、[キューに入れられたジョブとデータベース トランザクション](/docs/{{version}}/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="authorizing-channels"></a>
## チャネルの承認 (Authorizing Channels)

プライベート チャネルでは、現在認証されているユーザーが実際にチャネルをリッスンできることを承認する必要があります。これは、チャンネル名を使用して Laravel アプリケーションに HTTP リクエストを送信し、ユーザーがそのチャンネルでリッスンできるかどうかをアプリケーションが判断できるようにすることで実現されます。 [Laravel Echo](#client-side-installation) を使用すると、プライベート チャネルへのサブスクリプションを承認する HTTP リクエストが自動的に作成されます。ただし、これらのリクエストに応答するために適切なルートを定義する必要があります。

<a name="defining-authorization-routes"></a>
### 認可ルートの定義

ありがたいことに、Laravel では、チャネル承認リクエストに応答するルートを簡単に定義できます。 Laravel アプリケーションに含まれる `App\Providers\BroadcastServiceProvider` には、`Broadcast::routes` メソッドの呼び出しが表示されます。このメソッドは、認可リクエストを処理するために `/broadcasting/auth` ルートを登録します。

    Broadcast::routes();

`Broadcast::routes` メソッドは、そのルートを `web` ミドルウェア グループ内に自動的に配置します。ただし、割り当てられた属性をカスタマイズしたい場合は、ルート属性の配列をメソッドに渡すことができます。

    Broadcast::routes($attributes);

<a name="customizing-the-authorization-endpoint"></a>
#### 認可エンドポイントのカスタマイズ

デフォルトでは、Echo は `/broadcasting/auth` エンドポイントを使用してチャネル アクセスを承認します。ただし、`authEndpoint` 構成オプションを Echo インスタンスに渡すことで、独自の認証エンドポイントを指定できます。

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>
#### 認可リクエストのカスタマイズ

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
### 認可コールバックの定義

次に、現在認証されているユーザーが特定のチャンネルを聞くことができるかどうかを実際に判断するロジックを定義する必要があります。これは、アプリケーションに含まれる `routes/channels.php` ファイルで行われます。このファイルでは、`Broadcast::channel` メソッドを使用してチャネル承認コールバックを登録できます。

    use App\Models\User;

    Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
        return $user->id === Order::findOrNew($orderId)->user_id;
    });

`channel` メソッドは、チャネルの名前と、ユーザーがチャネルでリッスンする権限があるかどうかを示す `true` または `false` を返すコールバックの 2 つの引数を受け入れます。

すべての認可コールバックは、現在認証されているユーザーを最初の引数として受け取り、追加のワイルドカード パラメーターを後続の引数として受け取ります。この例では、`{orderId}` プレースホルダーを使用して、チャネル名の「ID」部分がワイルドカードであることを示しています。

`channel:list` Artisan コマンドを使用して、アプリケーションのブロードキャスト認証コールバックのリストを表示できます。

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 認可コールバックモデルバインディング

HTTP ルートと同様に、チャネル ルートも暗黙的および明示的な [ルートモデルバインディング](/docs/{{version}}/routing#route-model-binding) を利用できます。たとえば、文字列または数値の注文 ID を受け取る代わりに、実際の `Order` モデル インスタンスをリクエストできます。

    use App\Models\Order;
    use App\Models\User;

    Broadcast::channel('orders.{order}', function (User $user, Order $order) {
        return $user->id === $order->user_id;
    });

> [!WARNING]  
> HTTP ルート モデル バインディングとは異なり、チャネル モデル バインディングは自動 [暗黙的なモデルバインディングのスコープ設定](/docs/{{version}}/routing#implicit-model-binding-scoping) をサポートしません。ただし、ほとんどのチャネルは単一モデルの一意の主キーに基づいてスコープを設定できるため、これが問題になることはほとんどありません。

<a name="authorization-callback-authentication"></a>
#### 認可コールバック認証

プライベート ブロードキャスト チャネルとプレゼンス ブロードキャスト チャネルは、アプリケーションのデフォルトの認証ガードを介して現在のユーザーを認証します。ユーザーが認証されていない場合、チャネル承認は自動的に拒否され、承認コールバックは実行されません。ただし、必要に応じて、受信リクエストを認証する複数のカスタム ガードを割り当てることができます。

    Broadcast::channel('channel', function () {
        // ...
    }, ['guards' => ['web', 'admin']]);

<a name="defining-channel-classes"></a>
### チャネルクラスの定義

アプリケーションがさまざまなチャネルを使用している場合、`routes/channels.php` ファイルが大きくなる可能性があります。したがって、クロージャを使用してチャネルを承認する代わりに、チャネル クラスを使用することもできます。チャネル クラスを生成するには、`make:channel` Artisan コマンドを使用します。このコマンドは、新しいチャネル クラスを `App/Broadcasting` ディレクトリに配置します。

```shell
php artisan make:channel OrderChannel
```

次に、`routes/channels.php` ファイルにチャンネルを登録します。

    use App\Broadcasting\OrderChannel;

    Broadcast::channel('orders.{order}', OrderChannel::class);

最後に、チャネル クラスの `join` メソッドにチャネルの承認ロジックを配置できます。この `join` メソッドには、通常チャネル承認クロージャに配置するのと同じロジックが格納されます。チャネル モデル バインディングを利用することもできます。

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

> [!NOTE]  
> Laravel の他の多くのクラスと同様に、チャネル クラスは [サービスコンテナ](/docs/{{version}}/container) によって自動的に解決されます。したがって、コンストラクターでチャネルに必要な依存関係をタイプヒントで指定できます。

<a name="broadcasting-events"></a>
## イベントの放送 (Broadcasting Events)

イベントを定義し、それを `ShouldBroadcast` インターフェイスでマークしたら、あとはイベントのディスパッチ メソッドを使用してイベントを起動するだけです。イベント ディスパッチャは、イベントが `ShouldBroadcast` インターフェイスでマークされていることを認識し、ブロードキャスト用にイベントをキューに入れます。

    use App\Events\OrderShipmentStatusUpdated;

    OrderShipmentStatusUpdated::dispatch($order);

<a name="only-to-others"></a>
### 他人だけに

イベント ブロードキャストを利用するアプリケーションを構築する場合、現在のユーザーを除く特定のチャネルのすべての加入者にイベントをブロードキャストすることが必要になる場合があります。これは、`broadcast` ヘルパと `toOthers` メソッドを使用して実現できます。

    use App\Events\OrderShipmentStatusUpdated;

    broadcast(new OrderShipmentStatusUpdated($update))->toOthers();

`toOthers` メソッドを使用する必要がある場合をよりよく理解するために、ユーザーがタスク名を入力して新しいタスクを作成できるタスク リスト アプリケーションを想像してみましょう。タスクを作成するために、アプリケーションは、タスクの作成をブロードキャストし、新しいタスクの JSON 表現を返す `/task` URL にリクエストを行うことがあります。 JavaScript アプリケーションがエンドポイントから応答を受け取ると、次のように新しいタスクをタスク リストに直接挿入することがあります。

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

ただし、タスクの作成もブロードキャストすることに注意してください。タスク リストにタスクを追加するために JavaScript アプリケーションもこのイベントをリッスンしている場合、リストには重複したタスク (エンドポイントからのタスクとブロードキャストからのタスク) が 1 つずつ存在することになります。これを解決するには、`toOthers` メソッドを使用して、現在のユーザーにイベントをブロードキャストしないようにブロードキャスタに指示します。

> [!WARNING]  
> `toOthers` メソッドを呼び出すには、イベントで `Illuminate\Broadcasting\InteractsWithSockets` 特性を使用する必要があります。

<a name="only-to-others-configuration"></a>
#### 構成

Laravel Echo インスタンスを初期化すると、接続にソケット ID が割り当てられます。グローバル [Axios](https://github.com/mzabriskie/axios) インスタンスを使用して JavaScript アプリケーションから HTTP リクエストを作成している場合、ソケット ID はすべての発信リクエストに `X-Socket-ID` ヘッダーとして自動的に付加されます。次に、`toOthers` メソッドを呼び出すと、Laravel はヘッダーからソケット ID を抽出し、そのソケット ID を持つ接続にブロードキャストしないようにブロードキャスタに指示します。

グローバル Axios インスタンスを使用していない場合は、すべての送信リクエストで `X-Socket-ID` ヘッダーを送信するように JavaScript アプリケーションを手動で構成する必要があります。 `Echo.socketId` メソッドを使用してソケット ID を取得できます。

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 接続のカスタマイズ

アプリケーションが複数のブロードキャスト接続と対話し、デフォルト以外のブロードキャスタを使用してイベントをブロードキャストしたい場合は、`via` メソッドを使用してイベントをプッシュする接続を指定できます。

    use App\Events\OrderShipmentStatusUpdated;

    broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');

あるいは、イベントのコンストラクター内で `broadcastVia` メソッドを呼び出して、イベントのブロードキャスト接続を指定することもできます。ただし、これを行う前に、イベント クラスが `InteractsWithBroadcasting` 特性を使用していることを確認する必要があります。

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

<a name="receiving-broadcasts"></a>
## ブロードキャストを受信する (Receiving Broadcasts)

<a name="listening-for-events"></a>
### イベントをリッスンする

[Laravel Echoのインストールとインスタンス化](#client-side-installation) を取得したら、Laravel アプリケーションからブロードキャストされるイベントのリッスンを開始する準備が整います。まず、`channel` メソッドを使用してチャネルのインスタンスを取得し、次に `listen` メソッドを呼び出して指定されたイベントをリッスンします。

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

プライベート チャネルでイベントをリッスンする場合は、代わりに `private` メソッドを使用してください。 `listen` メソッドへの呼び出しを連鎖して、単一のチャネルで複数のイベントをリッスンすることもできます。

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### イベントの待機を停止する

[チャンネルを離れる](#leaving-a-channel) を使用せずに特定のイベントのリッスンを停止したい場合は、`stopListening` メソッドを使用できます。

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>
### チャンネルを離れる

チャンネルを離れるには、Echo インスタンスで `leaveChannel` メソッドを呼び出します。

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

チャネル、およびそれに関連付けられたプライベート チャネルおよびプレゼンス チャネルから脱退したい場合は、`leave` メソッドを呼び出すことができます。

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 名前空間

上記の例で、イベント クラスに完全な `App\Events` 名前空間を指定していないことに気づいたかもしれません。これは、Echo がイベントが `App\Events` 名前空間にあると自動的に想定するためです。ただし、Echo をインスタンス化するときに、`namespace` 構成オプションを渡すことでルート名前空間を構成できます。

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

あるいは、Echo を使用してイベント クラスをサブスクライブするときに、イベント クラスのプレフィックスとして `.` を付けることもできます。これにより、常に完全修飾クラス名を指定できるようになります。

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="presence-channels"></a>
## プレゼンスチャンネル (Presence Channels)

プレゼンス チャネルは、プライベート チャネルのセキュリティに基づいて構築されると同時に、誰がチャネルに登録しているかを認識する追加機能を公開します。これにより、別のユーザーが同じページを表示しているときにユーザーに通知したり、チャット ルームの住民をリストしたりするなど、強力な共同アプリケーション機能を簡単に構築できます。

<a name="authorizing-presence-channels"></a>
### プレゼンスチャネルの承認

すべてのプレゼンス チャネルはプライベート チャネルでもあります。したがって、ユーザーは [それらへのアクセスを許可されている](#authorizing-channels) である必要があります。ただし、プレゼンス チャネルの承認コールバックを定義する場合、ユーザーがチャネルへの参加を承認されている場合は、`true` は返されません。代わりに、ユーザーに関するデータの配列を返す必要があります。

承認コールバックによって返されたデータは、JavaScript アプリケーションのプレゼンス チャネル イベント リスナで利用できるようになります。ユーザーがプレゼンス チャネルに参加する権限を持たない場合は、`false` または `null` を返す必要があります。

    use App\Models\User;

    Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
        if ($user->canJoinRoom($roomId)) {
            return ['id' => $user->id, 'name' => $user->name];
        }
    });

<a name="joining-presence-channels"></a>
### プレゼンスチャンネルへの参加

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

`here` コールバックは、チャネルに正常に参加するとすぐに実行され、現在チャネルに登録している他のすべてのユーザーのユーザー情報を含む配列を受け取ります。 `joining` メソッドは、新しいユーザーがチャンネルに参加するときに実行され、`leaving` メソッドはユーザーがチャンネルを離れるときに実行されます。 `error` メソッドは、認証エンドポイントが 200 以外の HTTP ステータス コードを返した場合、または返された JSON の解析に問題があった場合に実行されます。

<a name="broadcasting-to-presence-channels"></a>
### プレゼンスチャネルへのブロードキャスト

プレゼンス チャネルは、パブリック チャネルまたはプライベート チャネルと同様にイベントを受信できます。チャットルームの例を使用すると、`NewMessage` イベントをルームのプレゼンス チャネルにブロードキャストすることができます。これを行うには、イベントの `broadcastOn` メソッドから `PresenceChannel` のインスタンスを返します。

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

他のイベントと同様に、`broadcast` ヘルパと `toOthers` メソッドを使用して、現在のユーザーをブロードキャストの受信から除外できます。

    broadcast(new NewMessage($message));

    broadcast(new NewMessage($message))->toOthers();

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
## モデル放送 (Model Broadcasting)

> [!WARNING]  
> モデルブロードキャストに関する以下のドキュメントを読む前に、Laravel のモデルブロードキャストサービスの一般的な概念とブロードキャストイベントを手動で作成してリッスンする方法を理解しておくことをお勧めします。

アプリケーションの [Eloquent モデル](/docs/{{version}}/eloquent) が作成、更新、または削除されたときにイベントをブロードキャストするのが一般的です。もちろん、これは手動で [Eloquent モデルの状態変更のカスタム イベントの定義](/docs/{{version}}/eloquent#events) を実行し、それらのイベントを `ShouldBroadcast` インターフェイスでマークすることで簡単に実現できます。

ただし、これらのイベントをアプリケーション内の他の目的で使用していない場合、イベントをブロードキャストすることだけを目的としてイベント クラスを作成するのは面倒になる可能性があります。これを解決するために、Laravel では、Eloquent モデルが状態の変更を自動的にブロードキャストする必要があることを示すことができます。

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

モデルにこの特性が含まれ、ブロードキャスト チャネルが定義されると、モデル インスタンスが作成、更新、削除、破棄、または復元されたときに、イベントのブロードキャストが自動的に開始されます。

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
#### モデルブロードキャストイベントの作成のカスタマイズ

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
### モデル放送規約

<a name="model-broadcasting-channel-conventions"></a>
#### チャネルの規則

お気づきかと思いますが、上記のモデル例の `broadcastOn` メソッドは `Channel` インスタンスを返しませんでした。代わりに、Eloquent モデルが直接返されました。 Eloquent モデルインスタンスがモデルの `broadcastOn` メソッドによって返される (またはメソッドによって返される配列に含まれる) 場合、Laravel はモデルのクラス名と主キー識別子をチャネル名として使用して、モデルのプライベートチャネルインスタンスを自動的にインスタンス化します。

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

モデルの `broadcastOn` メソッドからチャネル インスタンスを明示的に返す予定の場合は、Eloquent モデル インスタンスをチャネルのコンストラクターに渡すことができます。その際、Laravel は上で説明したモデル チャネル規則を使用して、Eloquent モデルをチャネル名の文字列に変換します。

```php
return [new Channel($this->user)];
```

モデルのチャネル名を決定する必要がある場合は、任意のモデル インスタンスで `broadcastChannel` メソッドを呼び出すことができます。たとえば、このメソッドは、`1` の `id` を持つ `App\Models\User` モデルの文字列 `App.Models.User.1` を返します。

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>
#### イベント規約

モデル ブロードキャスト イベントは、アプリケーションの `App\Events` ディレクトリ内の「実際の」イベントに関連付けられていないため、規則に基づいて名前とペイロードが割り当てられます。 Laravel の規則では、モデルのクラス名 (名前空間は含まない) とブロードキャストをトリガーしたモデル イベントの名前を使用してイベントをブロードキャストします。

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

`App\Models\User` モデルを削除すると、`UserDeleted` という名前のイベントがブロードキャストされます。

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
### モデルブロードキャストを聞く

`BroadcastsEvents` 特性をモデルに追加し、モデルの `broadcastOn` メソッドを定義したら、クライアント側アプリケーション内でブロードキャストされたモデル イベントのリッスンを開始する準備が整います。始める前に、[イベントをリッスンする](#listening-for-events) の完全なドキュメントを参照してください。

まず、`private` メソッドを使用してチャネルのインスタンスを取得し、次に `listen` メソッドを呼び出して指定されたイベントをリッスンします。通常、`private` メソッドに指定されるチャネル名は、Laravel の [モデルブロードキャスト規約](#model-broadcasting-conventions) に対応する必要があります。

チャネル インスタンスを取得したら、`listen` メソッドを使用して特定のイベントをリッスンできます。モデル ブロードキャスト イベントは、アプリケーションの `App\Events` ディレクトリ内の「実際の」イベントに関連付けられていないため、特定の名前空間に属していないことを示すために、[イベント名](#model-broadcasting-event-conventions) の先頭に `.` を付ける必要があります。各モデルのブロードキャスト イベントには、モデルのブロードキャスト可能なプロパティがすべて含まれる `model` プロパティがあります。

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>
## クライアントイベント (Client Events)

> [!NOTE]  
> [Pusher Channels](https://pusher.com/channels) を使用する場合、クライアント イベントを送信するには、[アプリケーションダッシュボード](https://dashboard.pusher.com/) の [アプリ設定] セクションで [クライアント イベント] オプションを有効にする必要があります。

Laravel アプリケーションをまったく起動せずに、接続されている他のクライアントにイベントをブロードキャストしたい場合があります。これは、「入力」通知など、別のユーザーが特定の画面でメッセージを入力していることをアプリケーションのユーザーに警告する場合に特に便利です。

クライアント イベントをブロードキャストするには、Echo の `whisper` メソッドを使用できます。

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

クライアント イベントをリッスンするには、`listenForWhisper` メソッドを使用できます。

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>
## 通知 (Notifications)

イベント ブロードキャストと [notifications](/docs/{{version}}/notifications) を組み合わせることにより、JavaScript アプリケーションは、ページを更新しなくても、新しい通知が発生したときに受信できるようになります。始める前に、[ブロードキャスト通知チャネル](/docs/{{version}}/notifications#broadcast-notifications) の使用に関するドキュメントを必ずお読みください。

ブロードキャスト チャネルを使用するように通知を構成したら、Echo の `notification` メソッドを使用してブロードキャスト イベントをリッスンできます。チャネル名は、通知を受信するエンティティのクラス名と一致する必要があることに注意してください。

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

この例では、`broadcast` チャネル経由で `App\Models\User` インスタンスに送信されたすべての通知がコールバックによって受信されます。 `App.Models.User.{id}` チャネルのチャネル認証コールバックは、Laravel フレームワークに付属するデフォルトの `BroadcastServiceProvider` に含まれています。

