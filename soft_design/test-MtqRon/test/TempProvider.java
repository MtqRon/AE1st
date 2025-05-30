package test;

import java.util.ArrayList;
import java.util.Iterator;

public abstract class TempProvider {
    private ArrayList observers = new ArrayList();        // Observerたちを保持
    public void addObserver(Observer observer) {    // Observerを追加
        observers.add(observer);
    }
    public void deleteObserver(Observer observer) { // Observerを削除
        observers.remove(observer);
    }
    public void notifyObservers() {               // Observerへ通知
        Iterator it = observers.iterator();
        while (it.hasNext()) {
            Observer o = (Observer)it.next();
            o.update(this);
        }
    }
    public abstract int getMaxTemp();            // 最高気温を取得する
    public abstract void execute();              // 気温を更新し知らせる
}
