// DeepL翻訳ヘルパー - 最終版
// 確実に動作する最小構成

console.log('DeepL翻訳ヘルパー最終版が開始されました');

// 拡張機能インストール時の処理
chrome.runtime.onInstalled.addListener(function() {
  console.log('拡張機能がインストールされました');
  
  // 既存メニューを削除
  chrome.contextMenus.removeAll(function() {
    console.log('既存メニューを削除しました');
    
    // 基本的な翻訳メニューを作成
    chrome.contextMenus.create({
      id: "translate-ja-en",
      title: "日本語→英語で翻訳",
      contexts: ["selection"]
    }, function() {
      if (chrome.runtime.lastError) {
        console.error('メニュー1作成エラー:', chrome.runtime.lastError);
      } else {
        console.log('日本語→英語メニューを作成しました');
      }
    });
    
    chrome.contextMenus.create({
      id: "translate-en-ja", 
      title: "英語→日本語で翻訳",
      contexts: ["selection"]
    }, function() {
      if (chrome.runtime.lastError) {
        console.error('メニュー2作成エラー:', chrome.runtime.lastError);
      } else {
        console.log('英語→日本語メニューを作成しました');
      }
    });
    
    chrome.contextMenus.create({
      id: "translate-auto",
      title: "自動検出で翻訳", 
      contexts: ["selection"]
    }, function() {
      if (chrome.runtime.lastError) {
        console.error('メニュー3作成エラー:', chrome.runtime.lastError);
      } else {
        console.log('自動検出メニューを作成しました');
      }
    });
  });
});

// メニュークリック時の処理
chrome.contextMenus.onClicked.addListener(function(info, tab) {
  console.log('メニューがクリックされました:', info.menuItemId);
  
  if (!info.selectionText) {
    console.log('選択されたテキストがありません');
    return;
  }
  
  const selectedText = info.selectionText.trim();
  if (!selectedText) {
    console.log('テキストが空です');
    return;
  }
  
  let fromLang = 'ja';
  let toLang = 'en';
  
  // メニューIDに基づいて言語を設定
  if (info.menuItemId === 'translate-ja-en') {
    fromLang = 'ja';
    toLang = 'en';
  } else if (info.menuItemId === 'translate-en-ja') {
    fromLang = 'en'; 
    toLang = 'ja';
  } else if (info.menuItemId === 'translate-auto') {
    fromLang = 'auto';
    toLang = 'ja';
  }
  
  // DeepLのURLを作成
  const deeplUrl = 'https://www.deepl.com/translator#' + fromLang + '/' + toLang + '/' + encodeURIComponent(selectedText);
  
  console.log('作成されたURL:', deeplUrl);
  
  // 既存のDeepLタブを探す
  chrome.tabs.query({url: "https://www.deepl.com/*"}, function(existingTabs) {
    if (existingTabs && existingTabs.length > 0) {
      // 既存のDeepLタブが見つかった場合、最初のタブを更新
      const existingTab = existingTabs[0];
      console.log('既存のDeepLタブを再利用します:', existingTab.id);
      
      chrome.tabs.update(existingTab.id, {
        url: deeplUrl,
        active: true
      }, function(updatedTab) {
        if (chrome.runtime.lastError) {
          console.error('タブ更新エラー:', chrome.runtime.lastError);
        } else {
          console.log('既存タブを更新しました:', updatedTab.id);
        }
      });
    } else {
      // 既存のDeepLタブがない場合、新しいタブを作成
      console.log('既存のDeepLタブが見つからないため、新しいタブを作成します');
      
      chrome.tabs.create({
        url: deeplUrl,
        active: true
      }, function(newTab) {
        if (chrome.runtime.lastError) {
          console.error('タブ作成エラー:', chrome.runtime.lastError);
        } else {
          console.log('新しいタブを作成しました:', newTab.id);
        }
      });
    }
  });
});
