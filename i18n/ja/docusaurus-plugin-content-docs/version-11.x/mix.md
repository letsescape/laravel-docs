# Laravel Mix (Laravel Mix)

- [Introduction](#introduction)

<a name="introduction"></a>
## 導入 (Introduction)

[Laracasts](https://github.com/laravel-mix/laravel-mix) の作成者である Jeffrey Way によって開発されたパッケージである [Laravel Mix](https://laracasts.com) は、いくつかの一般的な CSS および JavaScript プリプロセッサを使用して、Laravel アプリケーションの [webpack](https://webpack.js.org) ビルドステップを定義するための流暢な API を提供します。

言い換えれば、Mix を使用すると、アプリケーションの CSS ファイルと JavaScript ファイルのコンパイルと縮小が簡単になります。シンプルなメソッドチェーンを通じて、アセットパイプラインをスムーズに定義できます。例えば：

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

Webpack とアセットのコンパイルを開始する際に混乱したり圧倒されたりしたことがあれば、Laravel Mix を気に入るはずです。ただし、アプリケーションの開発中にこれを使用する必要はありません。希望するアセット パイプライン ツールを自由に使用することも、まったく使用しないこともできます。

> [!NOTE]  
> Vite は、新しい Laravel インストールで Laravel Mix を置き換えました。 Mix のドキュメントについては、[公式 Laravel Mix](https://laravel-mix.com/) Web サイトをご覧ください。 Vite に切り替えたい場合は、[Vite 移行ガイド](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite) をご覧ください。

