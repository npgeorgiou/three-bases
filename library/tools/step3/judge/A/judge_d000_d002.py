import json, os
BASE = "/home/claude/three-bases/library/tools/step3/judge"
ANS = {
"d000": "9384:y 9385:n 9386:y 9387:y 9406:n 9407:n 9408:n 9244:n 9245:n 9246:n 9247:n 9297:y 9298:y 9250:n 9295:n 9296:y 9282:y 9283:y 9284:y 9285:y 9305:y 9306:y 9307:y 9230:y 9403:n 9404:n 9405:n 9409:y 9410:y 9411:y 9412:y 9413:y 9275:y 9276:y 9277:y 9278:y 9279:y 9280:y 9281:y 9234:n 9235:n 9236:n 9237:n 9376:n 9377:y 9378:n 9379:y 9380:n 9381:y 9348:n 9349:y 9350:n 9351:n 9352:n 9353:n 9354:n 9356:n 9357:n 9370:n 9318:y 9252:y 9253:n 9254:y 9363:y 9364:y 9365:y 9238:n 9355:n 9291:y 9292:y 9293:y 9294:y 9345:n 9216:n 9217:y 9218:y 9219:n 9371:y 9372:y 9373:y",
"d001": "9374:y 9375:y 9366:y 9367:n 9368:n 9369:y 9396:y 9397:y 9398:n 9399:y 9392:n 9393:n 9394:n 9395:n 9329:n 9330:n 9331:n 9332:y 9333:n 9334:y 9335:y 9336:y 9337:y 9239:n 9240:n 9241:n 9242:n 9243:y 9255:y 9256:n 9257:n 9258:n 9248:n 9249:n 9251:y 9328:n 9290:y 9267:y 9268:y 9269:y 9270:y 9271:y 9272:y 9273:y 9274:y 9259:y 9260:y 9261:y 9262:y 9263:y 9264:y 9265:y 9266:y 9319:y 9320:y 9321:y 9322:y 9323:y 9324:y 9220:y 9221:y 9222:y 9223:y 9317:y 9299:y 9300:y 9301:y 9302:n 9303:y 9304:y 9231:n 9346:n 9347:n 9400:y 9401:n 9402:n 9325:n 9326:n 9327:n 9286:y",
"d002": "9287:y 9288:y 9289:y 9382:y 9383:y 9224:y 9225:y 9226:y 9342:y 9343:y 9344:y 9388:n 9389:n 9390:n 9391:n 9316:y 9358:y 9359:y 9360:y 9361:y 9362:y 9310:y 9311:n 9312:n 9313:n 9314:n 9315:y 9232:n 9233:n 9308:n 9309:n 9227:n 9228:n 9229:n 9338:y 9339:y 9340:y 9341:y",
}
os.makedirs(f"{BASE}/A", exist_ok=True)
for b, s in ANS.items():
    qs = []
    for line in open(f"{BASE}/{b}.txt", encoding="utf-8"):
        parts = line.rstrip("\n").split(" | ")
        if len(parts) >= 4 and parts[0].strip().isdigit() and False:
            pass
    # question lines are those after the '# questions' header with 5+ fields 'qid | concept | game | name | text'
    started = False
    for line in open(f"{BASE}/{b}.txt", encoding="utf-8"):
        if line.startswith("# questions"):
            started = True; continue
        if started and " | " in line:
            qs.append(line.split(" | ")[0].strip().rstrip("*"))
    pairs = [p.split(":") for p in s.split()]
    got = [q for q, _ in pairs]
    assert got == qs, (b, len(got), len(qs), [x for x in qs if x not in got][:5])
    out = {q: ("yes" if a == "y" else "no") for q, a in pairs}
    with open(f"{BASE}/A/{b}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=0)
    with open(f"{BASE}/A/progress_d.txt", "a", encoding="utf-8") as f:
        f.write(f"done {b}\n")
    print(b, len(out), "yes:", sum(v == "yes" for v in out.values()))
