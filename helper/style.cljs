(ns style.core
  (:require [reagent.core :as r] ))

(.log js/console "[init] style.core")

;; ;; Immutable initial state of the page.
;; (def page (.. js/document -documentElement -outerHTML))
;; ;; (def page (.serializeToString (new js/XMLSerializer) js/document))
;; (.log js/console page)
;; (.log js/console (clj->js (hk/as-hiccup (hk/parse page))))

;; (def toc (-> js/document -document getElementById "table-of-contents"))
;; (def toc (.getElementById js/document "table-of-contents"))


(def toc (.getElementById js/document "table-of-contents"))

(def node (.createElement js/document "BUTTON"))
(def textnode (.createTextNode js/document "This is a button."))
(.appendChild node textnode)

(.prepend toc node)
