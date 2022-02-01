// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface Xbas99LNexprn extends PsiElement {

  @Nullable
  Xbas99LFConst getFConst();

  @Nullable
  Xbas99LFNum getFNum();

  @NotNull
  List<Xbas99LFStr> getFStrList();

  @NotNull
  List<Xbas99LNexprn> getNexprnList();

  @Nullable
  Xbas99LNvarR getNvarR();

  @NotNull
  List<Xbas99LSexpr> getSexprList();

  @NotNull
  List<Xbas99LSvarR> getSvarRList();

}
