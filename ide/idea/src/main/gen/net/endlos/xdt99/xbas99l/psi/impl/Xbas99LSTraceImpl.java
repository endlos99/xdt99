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

public class Xbas99LSTraceImpl extends ASTWrapperPsiElement implements Xbas99LSTrace {

  public Xbas99LSTraceImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitSTrace(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99LVisitor) accept((Xbas99LVisitor)visitor);
    else super.accept(visitor);
  }

}