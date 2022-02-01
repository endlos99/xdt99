// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99l.psi.Xbas99LTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xbas99l.psi.*;

public class Xbas99LStatementXbImpl extends ASTWrapperPsiElement implements Xbas99LStatementXb {

  public Xbas99LStatementXbImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitStatementXb(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99LVisitor) accept((Xbas99LVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xbas99LBangComment getBangComment() {
    return findChildByClass(Xbas99LBangComment.class);
  }

  @Override
  @Nullable
  public Xbas99LSAccept getSAccept() {
    return findChildByClass(Xbas99LSAccept.class);
  }

  @Override
  @Nullable
  public Xbas99LSLinput getSLinput() {
    return findChildByClass(Xbas99LSLinput.class);
  }

  @Override
  @Nullable
  public Xbas99LSOnCond getSOnCond() {
    return findChildByClass(Xbas99LSOnCond.class);
  }

  @Override
  @Nullable
  public Xbas99LSRun getSRun() {
    return findChildByClass(Xbas99LSRun.class);
  }

  @Override
  @Nullable
  public Xbas99LSSub getSSub() {
    return findChildByClass(Xbas99LSSub.class);
  }

  @Override
  @Nullable
  public Xbas99LSSubend getSSubend() {
    return findChildByClass(Xbas99LSSubend.class);
  }

}
